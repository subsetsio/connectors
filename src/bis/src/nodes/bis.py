"""BIS (Bank for International Settlements) connector.

Mechanism: bulk_csv. BIS publishes one persistent zipped flat CSV per
statistical topic (SDMX dataflow) at
``https://data.bis.org/static/bulk/<DATAFLOW_ID>_csv_flat.zip``. Each topic is a
single full-table snapshot — no pagination, no auth. We re-fetch the whole
corpus every run (stateless full re-pull): the per-topic files are small-to-
moderate (a few hundred KB to ~350 MB zipped) and BIS revises history in place,
so a stored watermark would silently skip corrected observations. The largest
topics (locational/consolidated banking, debt securities) are streamed row by
row into row-group-batched Parquet so memory stays bounded.

The flat SDMX CSV layout is uniform across dataflows: ``STRUCTURE``,
``STRUCTURE_ID``, ``ACTION``, then the dataflow's *dimension* columns (which
differ per topic), then ``TIME_PERIOD``, ``OBS_VALUE``, then attribute columns.
We normalise every topic to one fixed long schema — dimensions are folded into a
``series_key`` (the colon-coded dimension values) plus a JSON ``dimensions`` map
— so a single uniform transform publishes each topic.
"""
import csv
import io
import json
import math
import os
import tempfile
import time
import zipfile

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    is_transient,
    raw_parquet_writer,
)

# The rank-accepted entity union — one BIS dataflow per id. Copied from
# data/sources/bis/work/entity_union.json. WS_NA_SEC_C3 is intentionally absent:
# the dataflow exists structurally but publishes no data (bulk file 404s and the
# SDMX /data endpoint returns "No data for data query"), so rank dropped it.
from constants import ENTITY_IDS

BULK_URL = "https://data.bis.org/static/bulk/{flow}_csv_flat.zip"

# Row-group batch size for streaming the (occasionally multi-GB uncompressed)
# flat CSV into Parquet without building the whole table in memory.
BATCH_ROWS = 100_000

# One fixed long schema for every topic. Per-topic dimension columns are folded
# into series_key + the dimensions JSON map, keeping the raw schema stable so the
# transform is uniform and parquet batches glob-union cleanly.
SCHEMA = pa.schema(
    [
        ("dataflow", pa.string()),
        ("series_key", pa.string()),
        ("freq", pa.string()),
        ("time_period", pa.string()),
        ("obs_value", pa.float64()),
        ("unit_measure", pa.string()),
        ("unit_mult", pa.string()),
        ("title", pa.string()),
        ("obs_status", pa.string()),
        ("dimensions", pa.string()),
    ]
)


# (connect, read) seconds. Read is generous: the largest topics are ~350 MB.
_TIMEOUT = (15.0, 600.0)
_DOWNLOAD_ATTEMPTS = 8
_CHUNK = 1 << 20  # 1 MiB


def _download_zip_to(url: str, dest_path: str) -> None:
    """Stream a bulk zip to ``dest_path``, resuming via HTTP Range on drops.

    BIS serves the largest topics (locational/consolidated banking ~350 MB) from
    a static host that occasionally closes the connection mid-body — a buffered
    ``.content`` read of the whole file then fails with RemoteProtocolError and a
    plain retry re-downloads from byte 0 (and tends to drop at the same offset).
    Instead we stream to disk and, on a transient drop, re-request only the
    missing tail with ``Range: bytes=<have>-``. We send ``Accept-Encoding:
    identity`` and use ``iter_raw`` so on-the-wire byte offsets match the file
    (a zip is already compressed, so the server returns it uncompressed anyway).
    """
    client = get_client()
    have = 0
    expected = None
    last_exc = None

    for attempt in range(_DOWNLOAD_ATTEMPTS):
        headers = {"Accept-Encoding": "identity"}
        if have:
            headers["Range"] = f"bytes={have}-"
        try:
            with client.stream("GET", url, headers=headers, timeout=_TIMEOUT) as resp:
                # Server ignored our Range (full 200 instead of 206 partial):
                # restart from scratch so we don't append a second full copy.
                if have and resp.status_code == 200:
                    have = 0
                # 416 = we already have the whole file; nothing left to fetch.
                if have and resp.status_code == 416:
                    return
                resp.raise_for_status()

                if expected is None:
                    cl = resp.headers.get("Content-Length")
                    # On a 206 the length is of the *remaining* range, so only
                    # trust Content-Length to set the total on a fresh 200.
                    if cl is not None and resp.status_code == 200:
                        expected = int(cl)

                mode = "ab" if have else "wb"
                with open(dest_path, mode) as fh:
                    for chunk in resp.iter_raw(_CHUNK):
                        fh.write(chunk)
                        have += len(chunk)

            # Stream ended cleanly. Guard against a silent short read.
            if expected is not None and have < expected:
                raise httpx.RemoteProtocolError(
                    f"short read: have {have} of {expected} bytes"
                )
            return
        except Exception as exc:  # noqa: BLE001 - re-raise non-transient below
            if not is_transient(exc):
                raise
            last_exc = exc
            # Exponential backoff, capped; keep `have` so we resume the tail.
            time.sleep(min(4 * 2 ** attempt, 120))

    raise last_exc


def _flow_from_node(node_id: str) -> str:
    # node id is f"bis-{flow.lower().replace('_', '-')}" -> recover the flow id.
    return node_id[len("bis-"):].upper().replace("-", "_")


def _code(value: str) -> str:
    # SDMX coded values look like "KW: Kuwait"; keep the code part ("KW").
    if not value:
        return ""
    return value.split(":", 1)[0].strip()


def _to_float(value: str):
    value = value.strip()
    if value == "":
        return None
    try:
        f = float(value)
    except ValueError:
        return None
    # BIS encodes missing/holiday/not-collected observations as the literal
    # string "NaN" (see OBS_STATUS M/L/H). float() happily parses those to a NaN
    # double, which is NOT NULL and would otherwise leak past the transform's
    # IS NOT NULL gate as a junk "observation". Treat any non-finite value as
    # missing so raw carries a clean None.
    if not math.isfinite(f):
        return None
    return f


def fetch_one(node_id: str) -> None:
    """Download one BIS topic's flat-CSV bulk zip and write normalised Parquet.

    Stateless full snapshot: the whole topic is re-fetched and overwritten every
    run. Freshness gating is the maintain step's job.
    """
    asset = node_id
    flow = _flow_from_node(node_id)

    fd, tmp_path = tempfile.mkstemp(prefix=f"{asset}-", suffix=".zip")
    os.close(fd)
    try:
        _download_zip_to(BULK_URL.format(flow=flow), tmp_path)
        with zipfile.ZipFile(tmp_path) as zf:
            _ingest_member(zf, zf.namelist()[0], asset, flow)
    finally:
        os.remove(tmp_path)


def _ingest_member(zf: zipfile.ZipFile, member: str, asset: str, flow: str) -> None:
    """Stream one flat-CSV member of a BIS bulk zip into normalised Parquet."""
    empty_batch = lambda: {name: [] for name in SCHEMA.names}
    batch = empty_batch()
    pending = 0

    with zf.open(member) as fh, raw_parquet_writer(asset, SCHEMA) as writer:
        text = io.TextIOWrapper(fh, encoding="utf-8-sig", newline="")
        reader = csv.reader(text)
        header = next(reader)

        # BIS does not quote the header's description labels, so a label that
        # contains commas (e.g. "STO:Stocks, Transactions, Other Flows" or
        # "EXPENDITURE:Expenditure (COFOG, COICOP, COPP or COPNI)") is split by
        # the CSV reader into spurious extra header cells, shifting every column
        # after it — TIME_PERIOD/OBS_VALUE then resolve to the wrong index and
        # obs_value reads empty. The real inter-column separator is a bare comma
        # while a comma inside a label is always followed by a space, so any
        # fragment beginning with whitespace is a continuation of the previous
        # cell. Data rows are properly quoted, so only the header needs repair.
        merged: list[str] = []
        for cell in header:
            if merged and cell[:1].isspace():
                merged[-1] = merged[-1] + "," + cell
            else:
                merged.append(cell)
        header = merged
        codes = [h.split(":", 1)[0].strip() for h in header]

        # SDMX flat layout: STRUCTURE, STRUCTURE_ID, ACTION, <dimensions...>,
        # TIME_PERIOD, OBS_VALUE, <attributes...>. Dimensions are the columns
        # between ACTION (index 2) and TIME_PERIOD; attributes follow OBS_VALUE.
        ti = codes.index("TIME_PERIOD")
        vi = codes.index("OBS_VALUE")
        dim_idx = list(range(3, ti))
        attr_idx = {codes[j]: j for j in range(vi + 1, len(codes))}
        freq_idx = codes.index("FREQ") if "FREQ" in codes else None
        title_idx = attr_idx.get("TITLE", attr_idx.get("TITLE_TS"))
        unit_idx = attr_idx.get("UNIT_MEASURE")
        mult_idx = attr_idx.get("UNIT_MULT")
        status_idx = attr_idx.get("OBS_STATUS")
        ncols = len(header)

        for row in reader:
            if len(row) < ncols:
                row = row + [""] * (ncols - len(row))

            # The bulk file interleaves series-metadata rows (no TIME_PERIOD,
            # no OBS_VALUE, attribute-only) with observation rows. They aren't
            # observations — keeping them pollutes the raw with empty-period
            # rows that collide on (series_key, time_period).
            if not row[ti].strip():
                continue

            dims = {codes[i]: row[i] for i in dim_idx}
            batch["dataflow"].append(flow)
            batch["series_key"].append(".".join(_code(row[i]) for i in dim_idx))
            batch["freq"].append(_code(row[freq_idx]) if freq_idx is not None else "")
            batch["time_period"].append(row[ti].strip())
            batch["obs_value"].append(_to_float(row[vi]))
            batch["unit_measure"].append(row[unit_idx] if unit_idx is not None else "")
            batch["unit_mult"].append(row[mult_idx] if mult_idx is not None else "")
            batch["title"].append(row[title_idx] if title_idx is not None else "")
            batch["obs_status"].append(row[status_idx] if status_idx is not None else "")
            batch["dimensions"].append(json.dumps(dims, ensure_ascii=False))
            pending += 1

            if pending >= BATCH_ROWS:
                writer.write_table(pa.table(batch, schema=SCHEMA))
                batch = empty_batch()
                pending = 0

        if pending:
            writer.write_table(pa.table(batch, schema=SCHEMA))


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"bis-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One uniform transform per topic. Thin parse-and-type pass: keep the canonical
# SDMX time_period string, drop missing observations, and derive a best-effort
# period_start DATE per frequency (NULL for frequencies we don't map). Every
# raw column is already typed at fetch time, so the transform only projects.
_TRANSFORM_SQL = '''
    SELECT
        dataflow,
        series_key,
        freq,
        time_period,
        CASE
            WHEN freq = 'D' THEN TRY_CAST(time_period AS DATE)
            WHEN freq = 'M' THEN TRY_STRPTIME(time_period || '-01', '%Y-%m-%d')::DATE
            WHEN freq = 'A' THEN TRY_STRPTIME(time_period || '-01-01', '%Y-%m-%d')::DATE
            WHEN freq = 'Q' THEN MAKE_DATE(
                TRY_CAST(SPLIT_PART(time_period, '-Q', 1) AS INTEGER),
                (TRY_CAST(SPLIT_PART(time_period, '-Q', 2) AS INTEGER) - 1) * 3 + 1,
                1)
            WHEN freq = 'H' THEN MAKE_DATE(
                TRY_CAST(SPLIT_PART(time_period, '-S', 1) AS INTEGER),
                (TRY_CAST(SPLIT_PART(time_period, '-S', 2) AS INTEGER) - 1) * 6 + 1,
                1)
            ELSE NULL
        END AS period_start,
        obs_value,
        unit_measure,
        unit_mult,
        title,
        obs_status,
        dimensions
    FROM "{dep}"
    WHERE obs_value IS NOT NULL AND isfinite(obs_value)
'''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=_TRANSFORM_SQL.format(dep=spec.id),
        key=("series_key", "time_period"),
        temporal="period_start",
    )
    for spec in DOWNLOAD_SPECS
]
