"""Bank of Japan — both published subsets (series catalog + values observations).

Two subsets share the same BOJ stat-search REST plumbing (see ``utils.py``):

``series`` is the catalog: one row per series_code (name, unit, frequency,
category, 5-level layer-tree position, recorded date range, last_update),
sourced from /getMetadata (one call per DB). Fetch shape: a stateless full
re-pull. Every refresh re-reads each DB's metadata and overwrites the catalog.
It is cheap (~50 small CSV calls) and picks up catalog edits/revisions for free.
Raw is written one parquet file per DB (``bank-of-japan-series-<db>``); the
transform glob-unions them.

``values`` is the observations: long-format (db, series_code, frequency,
survey_date, value, last_update), sourced from /getDataCode. The API exposes no
server-side ``since`` filter, so the node sweeps the full corpus, bucketed by
(db, frequency). Bucket state is checkpointed after each chunk so if the
supervisor interrupts the node the next run resumes from the unfinished bucket.
Completed buckets are re-pulled on the next invoked run so the current run has
inspectable raw batches for tests and transforms. Duplicate rows produced by
re-pulling a revised bucket are collapsed in the transform by keeping the
highest last_update per (db, series_code, survey_date).
getDataCode requires all codes in one request to share a frequency (hence
bucketing by frequency); it caps at 250 codes and 60000 data points per request,
paging the data-point overflow via NEXTPOSITION -> startPosition.
"""
import os
import re
import time

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    save_raw_parquet,
    load_state,
    save_state,
)

from utils import (
    DATABASES,
    _PermanentError,
    _data_block,
    _fetch_metadata,
    _request_csv,
    _to_int,
)

# ---------------------------------------------------------------------------
# series (catalog)
# ---------------------------------------------------------------------------

# Catalog (series) raw schema — declared once, the contract for every per-DB
# parquet batch. Dates are kept as raw YYYYMMDD strings and parsed in the
# transform (some are empty for layer-header rows / undated series).
SERIES_SCHEMA = pa.schema([
    ("db", pa.string()),
    ("series_code", pa.string()),
    ("name", pa.string()),
    ("unit", pa.string()),
    ("frequency", pa.string()),
    ("category", pa.string()),
    ("layer1", pa.string()),
    ("layer2", pa.string()),
    ("layer3", pa.string()),
    ("layer4", pa.string()),
    ("layer5", pa.string()),
    ("start_date", pa.string()),
    ("end_date", pa.string()),
    ("last_update", pa.string()),
    ("notes", pa.string()),
])


def fetch_series(node_id: str) -> None:
    for db in sorted(DATABASES):
        try:
            series = _fetch_metadata(db)
        except _PermanentError as exc:
            print(f"  skip catalog db={db}: {exc}")
            continue
        except httpx.HTTPStatusError as exc:
            print(f"  skip catalog db={db}: HTTP {exc.response.status_code}")
            continue
        if not series:
            print(f"  catalog db={db}: 0 series")
            continue
        table = pa.Table.from_pylist(series, schema=SERIES_SCHEMA)
        save_raw_parquet(table, f"{node_id}-{db.lower()}")


# ---------------------------------------------------------------------------
# values (observations)
# ---------------------------------------------------------------------------

# v2 flattened bucket progress from a single `buckets` dict into one top-level
# key per bucket. save_state diffs top-level keys and records the stringified
# old AND new value of each changed one; a single nested dict meant every
# per-chunk checkpoint appended two copies of the whole (growing) progress map,
# which is quadratic and overran the orchestrator's 10 MiB result-pickle cap.
#
# v3 scopes progress to RUN_ID and has the node request continuation before
# the GHA deadline. A failed/dead continuation leg may leave state behind
# without manifest-committed raw; cross-run resume from that state would skip
# raw files the transform cannot see.
STATE_VERSION = 3

# getDataCode hard caps: 250 codes per request (page the 60000-data-point
# overflow via NEXTPOSITION).
CODES_PER_CALL = 250

# Safety ceiling on NEXTPOSITION paging within one chunk — detects an
# unterminating cursor (source growth past expectations / API bug). Raises.
MAX_PAGES_PER_CHUNK = 2000

# Stay well clear of GitHub's hard cap and the orchestrator watchdog. The
# runtime treats a True return as needs_continuation and commits this leg's raw.
LEG_SECONDS = int(os.environ.get("BOJ_VALUES_LEG_SECONDS", str(4 * 60 * 60)))

# Observations (values) raw schema. survey_date / last_update are YYYYMMDD
# integers (well within int32); value is the observation (null obs are dropped
# at fetch time — they carry no information and bloat the raw).
VALUES_SCHEMA = pa.schema([
    ("db", pa.string()),
    ("series_code", pa.string()),
    ("frequency", pa.string()),
    ("survey_date", pa.int32()),
    ("value", pa.float64()),
    ("last_update", pa.int32()),
])


def _to_float(s: str):
    s = (s or "").strip()
    if not s or s.lower() == "null":
        return None
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def _freq_slug(freq: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (freq or "na").lower()).strip("-") or "na"


def _bucket_signature(series: list[dict]) -> str:
    max_lu = max((_to_int(s["last_update"]) or 0) for s in series)
    return f"{max_lu}:{len(series)}"


def _bucket_key(db: str, freq: str) -> str:
    """Top-level state key for one (db, frequency) bucket.

    One key per bucket, not one nested dict: save_state records the old and new
    value of every changed top-level key, so a per-chunk checkpoint must touch a
    small value. `_`-prefixed keys are reserved by the orchestrator.
    """
    return f"b:{db}|{freq}"


def _fetch_chunk_rows(db: str, freq: str, codes: list[str]) -> list[dict]:
    """All observations for `codes` (same frequency), paging NEXTPOSITION."""
    rows: list[dict] = []
    start_position = None
    pages = 0
    while True:
        params = {"db": db, "code": ",".join(codes)}
        if start_position:
            params["startPosition"] = start_position
        resp_rows = _request_csv("getDataCode", params)
        header, data, next_pos = _data_block(resp_rows)
        col = {name: header.index(name) for name in header}
        c_code = col.get("SERIES_CODE")
        c_date = col.get("SURVEY_DATES")
        c_val = col.get("VALUES")
        c_lu = col.get("LAST_UPDATE")
        for row in data:
            value = _to_float(row[c_val]) if c_val is not None and c_val < len(row) else None
            if value is None:
                continue  # drop null observations
            date = _to_int(row[c_date]) if c_date is not None and c_date < len(row) else None
            if date is None:
                continue
            rows.append({
                "db": db,
                "series_code": row[c_code] if c_code is not None and c_code < len(row) else "",
                "frequency": freq,
                "survey_date": date,
                "value": value,
                "last_update": _to_int(row[c_lu]) if c_lu is not None and c_lu < len(row) else None,
            })
        pages += 1
        if not next_pos:
            break
        if pages >= MAX_PAGES_PER_CHUNK:
            raise RuntimeError(
                f"getDataCode db={db} freq={freq} exceeded {MAX_PAGES_PER_CHUNK} "
                f"pages without terminating — possible cursor/source-growth bug"
            )
        start_position = next_pos
    return rows


def fetch_values(node_id: str) -> None:
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        if state:
            print(f"  state schema {state.get('schema_version')} != {STATE_VERSION}; resetting")
        state = {"schema_version": STATE_VERSION}
    run_id = os.environ.get("RUN_ID", "unknown")
    deadline = time.monotonic() + LEG_SECONDS

    # Sweep every database/frequency/chunk, but yield before the CI deadline.
    # Bucket state is checkpointed after each chunk and scoped to RUN_ID. Within
    # one continuation chain, completed buckets are skipped because their raw
    # is already manifest-committed by earlier legs. A fresh run re-pulls them.
    for db in sorted(DATABASES):
        try:
            series = _fetch_metadata(db)
        except _PermanentError as exc:
            print(f"  skip values db={db}: {exc}")
            continue
        except httpx.HTTPStatusError as exc:
            print(f"  skip values db={db}: HTTP {exc.response.status_code}")
            continue

        by_freq: dict[str, list[dict]] = {}
        for s in series:
            by_freq.setdefault(s["frequency"] or "NA", []).append(s)

        for freq, members in sorted(by_freq.items()):
            bucket_key = _bucket_key(db, freq)
            signature = _bucket_signature(members)
            prev = state.get(bucket_key, {})
            codes = sorted(m["series_code"] for m in members)
            freq_slug = _freq_slug(freq)
            chunks = [codes[i:i + CODES_PER_CALL]
                      for i in range(0, len(codes), CODES_PER_CALL)]
            same_run = (
                prev.get("run_id") == run_id
                and prev.get("sig") == signature
            )
            if same_run and prev.get("complete"):
                print(f"  skip values {bucket_key}: complete in this run")
                continue

            # Resume mid-bucket only inside the same continuation chain. A
            # completed prior run must not short-circuit this fetch: when the
            # node is invoked under a new RUN_ID, it needs to materialise raw
            # batches for that run so tests and transforms see a complete raw
            # manifest.
            start_chunk = (
                prev.get("done_chunks", 0)
                if same_run and not prev.get("complete")
                else 0
            )

            for ci in range(start_chunk, len(chunks)):
                if time.monotonic() >= deadline:
                    print(
                        f"  values leg budget spent before {bucket_key} chunk {ci}; "
                        "committing and continuing next link"
                    )
                    return True
                try:
                    rows = _fetch_chunk_rows(db, freq, chunks[ci])
                except _PermanentError as exc:
                    print(f"  skip values {bucket_key} chunk {ci}: {exc}")
                    rows = []
                except httpx.HTTPStatusError as exc:
                    print(f"  skip values {bucket_key} chunk {ci}: HTTP {exc.response.status_code}")
                    rows = []
                asset = f"{node_id}-{db.lower()}-{freq_slug}-{ci:04d}"
                table = pa.Table.from_pylist(rows, schema=VALUES_SCHEMA)
                save_raw_parquet(table, asset)  # write raw before advancing state
                state[bucket_key] = {
                    "run_id": run_id,
                    "sig": signature, "done_chunks": ci + 1,
                    "n_chunks": len(chunks), "complete": False,
                }
                save_state(node_id, state)  # checkpoint after each chunk

            state[bucket_key] = {
                "run_id": run_id,
                "sig": signature, "done_chunks": len(chunks),
                "n_chunks": len(chunks), "complete": True,
            }
            save_state(node_id, state)  # mark bucket fully pulled


# ---------------------------------------------------------------------------
# specs
# ---------------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="bank-of-japan-series", fn=fetch_series, kind="download"),
    NodeSpec(id="bank-of-japan-values", fn=fetch_values, kind="download"),
]
