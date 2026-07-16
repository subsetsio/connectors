"""Danmarks Nationalbank — StatBank tables via the api.statbank.dk v1 API.

Each of the ~107 'DN'-prefixed StatBank tables is one publishable subset. The
StatBank exposes them through the modern Statistics-Denmark JSON API:

  - GET  /v1/tableinfo/<id>  -> dimension variable codes (+ which is time)
  - POST /v1/data            -> the data, requested in 'BULK' format (no cell cap)

Fetch shape: **stateless full re-pull** (the default). Every refresh pulls each
table in its entirety and overwrites; no watermark is trusted, so revisions and
late corrections are picked up for free.

Why the data request is chunked: the BULK endpoint reliably 500s / drops the
connection (incomplete chunked read) when asked to stream a single
multi-hundred-MB response (several of these tables are 600MB-950MB as one
extract — DNSUBOH, DNVP2, DNVPDKF, DNVPDKR2). So instead of one POST with
Tid=["*"], we pull the table in slices kept to ~TARGET_ROWS rows each.

Why the non-time dimensions are requested as EXPLICIT value lists and never as
the "*" wildcard: several of these tables share one physical StatBank cube with
their siblings (DNRENTD/DNRENTM/DNRENTA are the daily/monthly/annual views of
one interest-rate cube; the DNVP* securities tables likewise). Each *table*
declares, via /v1/tableinfo, the subset of the cube it actually publishes. "*"
does NOT mean "the values this table declares" — it means "every value present
in the underlying cube", so it leaks cells belonging to the sibling tables'
series. Those leaked cells have no entry in this table's value table, so BULK
renders their dimension label as an EMPTY STRING (and `valuePresentation=Code`
blanks them too — they are unidentifiable in BULK by any means).

That is not a cosmetic defect. The leaked rows are indistinguishable from each
other, so a coordinate box can come back several times with a blank dimension
and different values, which destroys row identity: DNRENTD at 1983M05D10
returned 49 rows for 8 distinct coordinates (45 blank-labelled), DNBALA 2003M01
210 rows for 126 coordinates, DNVPU 2018M12 10,628 rows for 10,488. Downstream
this is exactly why the model could not settle a real grain (it had to pad every
key with the `value` MEASURE, and 18 tables ended up keyless).

The explicit list is the source's own answer: tableinfo, JSONSTAT and CSV all
return precisely the declared subset for the same request. Nothing is lost —
the leaked series are published by the sibling table that declares them (the
CSO10Y/CIT03M/CRO10Y yields DNRENTD leaks are declared by DNRENTM and DNRENTA,
which this connector also downloads).

The wildcard IS still correct for the time dimension: only one table owns a
given frequency, so Tid never leaks.

The slice size is set from *actual* row counts, not the dense cardinality
product: many tables are extremely sparse (e.g. DNVPDKR2's dense cross-product is
~100M cells, yet one month is only ~0.7M real rows in 158MB), so a dense estimate
either over-splits into hundreds of thousands of tiny requests or — worse —
under-splits because it can't see that a *single* period already blows past the
limit. We instead probe the most-recent (largest) period to learn rows/period,
then either pack several periods per request (small tables) or pull one period
at a time (giant tables).
Every fetch is additionally wrapped in a reactive splitter: if a slice still
drops after the transient retries, it is bisected along its widest axis and
retried, guaranteeing forward progress regardless of the size estimate.

Raw format: NDJSON (gzip). The tables are heterogeneous — each has its own
dimension list — and all cell fields are written as JSON strings (the StatBank
value field uses '..' for missing), so a fixed parquet schema would be wrong
here. The transform re-types the value column to DOUBLE.
"""

import json
import os
import time
from datetime import datetime, timezone

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    delete_raw_file,
    get,
    get_client,
    list_raw_fragments,
    raw_asset_exists,
    raw_manifest,
    transient_retry,
    raw_writer,
)
from constants import ENTITY_IDS

SLUG = "danmarks-nationalbank"
API = "https://api.statbank.dk/v1"

# Target *actual rows* per /v1/data request. Sized from a live probe (not the
# dense cardinality product). ~200k rows is a few tens of MB per response — well
# under the multi-hundred-MB single-shot extracts that make the server drop the
# connection, while keeping the request count sane for the giant sparse tables.
TARGET_ROWS = 200_000
# Safety ceiling on periods per slice, independent of the row estimate.
MAX_PERIODS_PER_CHUNK = 2_000
# Max recursive bisections in the reactive splitter before giving up.
MAX_SPLIT_DEPTH = 32
# Long StatBank securities tables can exceed one GitHub leg. Commit period
# fragments and checkpoint well before the runner deadline so the next leg
# resumes from the manifest instead of re-streaming the same data.
NODE_BUDGET_S = 1_200
COMPLETE_FRAGMENT = "_complete"


class PartialFetchError(RuntimeError):
    """A streamed response failed after rows were emitted to the current file."""


def _table_id(node_id: str) -> str:
    """Recover the StatBank table id from the node/asset id."""
    return node_id[len(SLUG) + 1:].upper().replace("-", "_")


@transient_retry()
def _tableinfo(table_id: str) -> dict:
    resp = get(f"{API}/tableinfo/{table_id}", params={"format": "JSON"}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _column_keys(header: str, time_codes: set) -> list:
    """Map BULK CSV header columns to JSON keys: value column -> 'value', the
    time dimension -> 'time', every other dimension -> its lowercased code."""
    keys = []
    for raw in header.split(";"):
        c = raw.strip()
        cu = c.upper()
        if cu == "INDHOLD":
            keys.append("value")
        elif cu in time_codes:
            keys.append("time")
        else:
            keys.append(c.lower())
    return keys


def _fetch_slice(body: dict, time_codes: set, emit) -> int:
    """Fetch one slice and stream parsed records to `emit`.

    The caller writes each committed slice as a raw fragment, so a failed slice
    leaks no partial data and successful slices stay bounded in memory.
    """
    rows = 0
    try:
        with get_client().stream("POST", f"{API}/data", json=body, timeout=(10.0, 600.0)) as resp:
            resp.raise_for_status()
            lines = resp.iter_lines()
            header = next(lines, None)
            if header is None:
                return rows
            keys = _column_keys(header, time_codes)
            ncols = len(keys)
            for line in lines:
                if not line:
                    continue
                parts = line.split(";")
                if len(parts) != ncols:
                    # Defensive: a stray embedded ';' would desync the row; skip it
                    # rather than silently mis-key columns.
                    continue
                emit({keys[i]: parts[i] for i in range(ncols)})
                rows += 1
    except Exception as exc:
        if rows:
            raise PartialFetchError(f"stream failed after {rows} emitted row(s)") from exc
        raise
    return rows


def _expanded_specs(var_specs: list, values_by_code: dict | None) -> list:
    if not values_by_code:
        return var_specs
    expanded = []
    for spec in var_specs:
        values = spec["values"]
        if values == ["*"]:
            values = values_by_code[spec["code"]]
        expanded.append({"code": spec["code"], "values": list(values)})
    return expanded


def _emit_box(
    table_id: str,
    var_specs: list,
    time_codes: set,
    emit,
    depth: int = 0,
    values_by_code: dict | None = None,
) -> None:
    """Fetch one box (explicit value lists on every dimension) and emit its rows.

    The reactive safety net: every dimension is passed as an explicit value list
    (never "*"), so if the request still drops after the transient retries, we
    bisect the widest axis and recurse on the halves — guaranteeing forward
    progress no matter how wrong the up-front size estimate was."""
    body = {"table": table_id, "lang": "en", "format": "BULK", "variables": var_specs}
    try:
        rows = _fetch_slice(body, time_codes, emit)
    except PartialFetchError:
        raise
    except Exception:
        var_specs = _expanded_specs(var_specs, values_by_code)
        widest = max(range(len(var_specs)), key=lambda i: len(var_specs[i]["values"]))
        if depth >= MAX_SPLIT_DEPTH or len(var_specs[widest]["values"]) < 2:
            raise
        vals = var_specs[widest]["values"]
        mid = len(vals) // 2
        for half in (vals[:mid], vals[mid:]):
            sub = [dict(s) for s in var_specs]
            sub[widest] = {"code": var_specs[widest]["code"], "values": half}
            _emit_box(table_id, sub, time_codes, emit, depth + 1, values_by_code)
        return
    return rows


def _fragment_name(periods: list[str]) -> str:
    if len(periods) == 1:
        return periods[0]
    return f"{periods[0]}--{periods[-1]}"


def _write_fragment(asset: str, fragment: str, fetch) -> int:
    written = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip", fragment=fragment) as f:
        def emit(rec):
            nonlocal written
            f.write(json.dumps(rec, separators=(",", ":")))
            f.write("\n")
            written += 1

        fetch(emit)
    return written


def _current_run_fragments(asset: str) -> set[str]:
    run_id = os.environ.get("RUN_ID", "unknown")
    return {
        frag
        for frag, meta in list_raw_fragments(asset, "ndjson.gz").items()
        if meta.get("run_id") == run_id
    }


def _start_fragment_run(asset: str, done: set[str]) -> None:
    # A fresh run must replace any previous full or fragmented extract. During
    # continuation legs, current-run fragments are present and must be kept.
    if done:
        return
    if list_raw_fragments(asset, "ndjson.gz"):
        delete_raw_file(asset, "ndjson.gz")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    table_id = _table_id(node_id)
    info = _tableinfo(table_id)
    variables = info["variables"]

    time_var = next((v for v in variables if v.get("time")), None)
    time_codes = {time_var["id"].upper()} if time_var else set()
    values_by_code = {
        v["id"]: [x["id"] for x in v["values"]]
        for v in variables
    }
    # Explicit value lists, never "*": the wildcard returns the whole shared
    # cube, including sibling tables' series, which BULK emits with a blank
    # (unrecoverable) dimension label. See the module docstring.
    nt_specs = [
        {"code": v["id"], "values": [x["id"] for x in v["values"]]}
        for v in variables if not v.get("time")
    ]

    if time_var is None:
        written = 0
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
            def emit(rec):
                nonlocal written
                f.write(json.dumps(rec, separators=(",", ":")))
                f.write("\n")
                written += 1

            _emit_box(table_id, nt_specs, time_codes, emit, values_by_code=values_by_code)
    else:
        done = _current_run_fragments(asset)
        if COMPLETE_FRAGMENT in done:
            return False
        _start_fragment_run(asset, done)

        time_code = time_var["id"]
        periods = [val["id"] for val in time_var["values"]]

        t0 = time.monotonic()
        written = 0

        # Probe the most-recent period unless a continuation leg already wrote
        # it. The probe is itself the period fragment; no duplicate request.
        recent = periods[-1]
        if recent not in done:
            written += _write_fragment(
                asset,
                recent,
                lambda emit: _emit_box(
                    table_id,
                    nt_specs + [{"code": time_code, "values": [recent]}],
                    time_codes,
                    emit,
                    values_by_code=values_by_code,
                ),
            )
            done.add(recent)
        rows_recent = max(1, written) if written else TARGET_ROWS + 1

        remaining = periods[:-1]
        if rows_recent <= TARGET_ROWS:
            per_chunk = min(MAX_PERIODS_PER_CHUNK, max(1, TARGET_ROWS // rows_recent))
            chunks = [remaining[i:i + per_chunk] for i in range(0, len(remaining), per_chunk)]
        else:
            chunks = [[p] for p in remaining]

        for chunk in reversed(chunks):  # newest first for useful partial progress
            fragment = _fragment_name(chunk)
            if fragment in done:
                continue
            written += _write_fragment(
                asset,
                fragment,
                lambda emit, chunk=chunk: _emit_box(
                        table_id,
                        nt_specs + [{"code": time_code, "values": chunk}],
                        time_codes,
                        emit,
                        values_by_code=values_by_code,
                ),
            )
            done.add(fragment)
            if time.monotonic() - t0 > NODE_BUDGET_S:
                return True

        _write_fragment(asset, COMPLETE_FRAGMENT, lambda emit: None)

    if written == 0:
        # An active table that yields no rows means the BULK contract changed.
        raise AssertionError(f"{table_id}: BULK extract produced 0 data rows")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Raw fetched before this instant was produced by the old wildcard fetch and
# carries the leaked, blank-labelled sibling-cube rows the module docstring
# describes. Such raw is wrong at any age, so the cadence skip must not honour
# it — otherwise the corrupt extract survives until it ages past the 7-day
# window and the fix silently does nothing. Self-expiring: once every asset has
# been refetched past this instant the clause never fires again, and it can be
# dropped along with the freshness join below.
_WILDCARD_FIX_AT = datetime(2026, 7, 14, 21, 0, tzinfo=timezone.utc)

_MAINTAIN_DESCRIPTION = (
    "Skip raw assets fetched within 7 days AND produced by the current "
    "explicit-value-list fetch; production cadence is weekly "
    "(maintenance.json cadence_days=7), and each run re-pulls the full StatBank table."
)


def _raw_is_current(asset_id: str) -> bool:
    if not raw_asset_exists(asset_id, "ndjson.gz", max_age_days=7):
        return False
    entry = raw_manifest.asset_entry(asset_id, "ndjson.gz")
    if entry is None:
        return False
    fragments = entry.get("fragments") or {}
    if "full" not in fragments and COMPLETE_FRAGMENT not in fragments:
        return False
    fetched = raw_manifest.newest_fetched_at(entry)
    # Unknown fetch time — refetch rather than trust a pre-fix extract.
    return fetched is not None and fetched >= _WILDCARD_FIX_AT


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=_MAINTAIN_DESCRIPTION,
        check=_raw_is_current,
    )
    for spec in DOWNLOAD_SPECS
]
