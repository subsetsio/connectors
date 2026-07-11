"""Open Power System Data (OPSD) connector — node module.

OPSD publishes Frictionless tabular-data-packages on its data platform. Each
collect entity is one CSV resource, identified as `<package>__<resource_stem>`,
served at:

    https://data.open-power-system-data.org/<package>/latest/<resource_stem>.csv

Fetch shape: **stateless full re-pull** (shape 1). Every CSV is a complete
snapshot of its table; OPSD releases new versions infrequently (roughly annual)
under the moving `latest/` alias, so each run re-downloads the current snapshot
in full and overwrites — no watermark, no incremental filter (the source exposes
none). The biggest table (hourly time_series, ~50k rows × 300 cols) is ~123MB in
memory, comfortably in RAM.

Raw format: the CSVs are double-quoted, single-header tabular files, but their
**dialect is not uniform** — most packages are comma-delimited with a `.` decimal
(e.g. `0.504`), while `when2heat` is semicolon-delimited with a `,` decimal
(e.g. `2,8` = 2.8), the European convention. We therefore sniff the delimiter
from the header line and pair `;`→decimal-comma / `,`→decimal-point, then let
DuckDB infer types over the *whole* file (`sample_size=-1`, VARCHAR fallback on
genuine mixing). `ignore_errors=true` drops the occasional structurally-broken
row (see below) in-engine rather than failing the whole table. The SQL transform
is then a thin pass-through that publishes the typed table verbatim.

A couple of OPSD tables (notably `renewable_power_plants_UK`, and one row of
`renewable_power_plants_DE`) contain a stray record with an *unquoted embedded
newline* — a non-RFC-4180 malformation. DE's single bad row is dropped in-engine
by `ignore_errors`; UK's breaks DuckDB's column-count auto-detection outright, so
`_csv_to_arrow` falls back to Python's lenient `csv` module: it keeps only
header-width rows (dropping the malformed fragments), rewrites a clean CSV, and
lets DuckDB infer types from that. Dropped-row counts are logged.
"""

import csv
import os
import tempfile

import duckdb

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_IDS

SLUG = "open-power-system-data"
BASE = "https://data.open-power-system-data.org"
# Generous ceiling: OPSD rows are short, but a malformed embedded newline can make
# DuckDB see one enormous "line" before it errors into the repair fallback.
MAX_LINE_SIZE = 10_000_000


def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# spec id -> original-cased collect entity id (the lower/replace mapping is lossy,
# so we keep the reverse map explicitly). Plain dict comprehension, no I/O.
ENTITY_BY_SPEC = {_spec_id(eid): eid for eid in ENTITY_IDS}


@transient_retry()
def _download_csv(url: str) -> bytes:
    # read timeout generous: the largest CSV (time_series_60min) is ~130MB.
    resp = get(url, timeout=(15.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _sniff_dialect(header_line: bytes) -> tuple[str, str]:
    """Decide (delimiter, decimal_separator) from the header line. OPSD packages
    are either comma-delimited with a '.' decimal, or (when2heat) semicolon-
    delimited with a ',' decimal — the European convention couples the two."""
    if header_line.count(b";") > header_line.count(b","):
        return ";", ","
    return ",", "."


def _duckdb_read(path: str, delim: str, decimal: str):
    """Parse a CSV to an Arrow table with full-file type inference. The Arrow
    path (vs fetchall) avoids the tz->python datetime materialization that would
    need pytz for timezone-aware columns.

    ignore_errors=true drops structurally-malformed rows in-engine (e.g. the
    single stray unquoted-embedded-newline record in renewable_power_plants_DE),
    so a 1.7M-row file never has to round-trip through Python. With sample_size=-1
    the inferred types fit every row (VARCHAR fallback on genuine mixing), so only
    column-count-broken rows are dropped, never well-formed ones. Gross drops are
    caught by the row_count expectations."""
    safe = path.replace("'", "''")
    con = duckdb.connect()
    try:
        return con.execute(
            f"""SELECT * FROM read_csv('{safe}',
                 delim='{delim}', quote='"', escape='"', header=true,
                 decimal_separator='{decimal}',
                 sample_size=-1, ignore_errors=true,
                 max_line_size={MAX_LINE_SIZE})"""
        ).fetch_arrow_table()
    finally:
        con.close()


def _repair_to_clean_csv(src_path: str, delim: str) -> tuple[str, int]:
    """Re-emit a strict CSV keeping only header-width rows. Drops any row whose
    field count differs from the header (the fragments left behind by an unquoted
    embedded newline). Returns (clean_path, n_dropped)."""
    with open(src_path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f, delimiter=delim))
    header = rows[0]
    width = len(header)
    good = [r for r in rows[1:] if len(r) == width]
    dropped = (len(rows) - 1) - len(good)
    clean = tempfile.NamedTemporaryFile(
        suffix=".csv", delete=False, mode="w", newline="", encoding="utf-8"
    )
    try:
        writer = csv.writer(clean, delimiter=delim)
        writer.writerow(header)
        writer.writerows(good)
    finally:
        clean.close()
    return clean.name, dropped


def _csv_to_arrow(tmp_path: str, asset: str):
    """Primary: parse with the sniffed dialect. Fallback: repair non-RFC-4180
    files via the csv module, then parse the cleaned copy."""
    with open(tmp_path, "rb") as f:
        header_line = f.readline()
    delim, decimal = _sniff_dialect(header_line)
    try:
        return _duckdb_read(tmp_path, delim, decimal)
    except duckdb.Error as exc:
        print(f"[{asset}] strict CSV parse failed ({type(exc).__name__}); "
              f"repairing with csv-module fallback")
        clean_path, dropped = _repair_to_clean_csv(tmp_path, delim)
        try:
            table = _duckdb_read(clean_path, delim, decimal)
        finally:
            if os.path.exists(clean_path):
                os.unlink(clean_path)
        print(f"[{asset}] repaired: {table.num_rows} rows kept, {dropped} malformed row(s) dropped")
        return table


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = ENTITY_BY_SPEC[node_id]
    package, stem = entity_id.split("__", 1)
    url = f"{BASE}/{package}/latest/{stem}.csv"

    content = _download_csv(url)

    # Write to a scratch temp file so DuckDB can do full-file type inference.
    # This is scratch I/O, not raw persistence — the raw asset is written via
    # save_raw_parquet below.
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        table = _csv_to_arrow(tmp_path, asset)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
