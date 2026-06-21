"""Central Bank (Taiwan) — CBC Statistical Database connector.

Mechanism (research id `datadb_rest`): the CBC Statistical Database at
cpx.cbc.gov.tw is a PC-Axis (PX) backed time-series DB. Each of the ~198
catalog leaves is one `.px` matrix, fetched in full from a single endpoint:

    GET https://cpx.cbc.gov.tw/api/DataAPI/Get?FileName=<code>

where <code> is the px filename without the `.px` suffix (e.g. EF01M01,
FL01_cn). One request returns the ENTIRE matrix as JSON:

    {meta: {title, units, last_updated, matrix, ...},
     data: {dataSets: [[period, v0, v1, ...], ...],
            structure: {Table1: [{data: label}], Table2: [...], ...}}}

`dataSets[*][0]` is the period label; the remaining cells are the cartesian
product of the dimension-member labels in `structure`, in C-order with Table1
outermost and the highest-numbered table innermost (verified live against
EF01M01). We melt each matrix into a uniform long table — one row per
(period, series) where `series` is the pipe-joined member labels — so a single
generic transform publishes all 198 heterogeneous matrices.

Fetch shape: stateless full re-pull. Every matrix is small (largest ~150k
cells) and the source has no incremental filter, so each run re-fetches the
whole table and overwrites. No auth, no documented rate limit (we still cap
concurrency politely via per-node subprocesses).
"""
import calendar
import itertools
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

SLUG = "central-bank-taiwan"
DATA_URL = "https://cpx.cbc.gov.tw/api/DataAPI/Get"

# Original px codes (the entity union). Spec ids lowercase them and map '_'->'-',
# so we keep this reverse map to recover the exact (case-sensitive) FileName.
from constants import ENTITY_IDS


def _spec_id(eid: str) -> str:
    return f"{SLUG}-{eid.lower().replace('_', '-')}"


CODE_BY_SPEC = {_spec_id(eid): eid for eid in ENTITY_IDS}

SCHEMA = pa.schema([
    ("period", pa.string()),   # source period label, verbatim (e.g. "1987M05")
    ("date", pa.string()),     # normalized ISO start-of-period date, or null
    ("series", pa.string()),   # pipe-joined dimension member labels
    ("value", pa.float64()),   # numeric value; null for missing-data tokens
])

# Tokens the source uses for "no data" in a numeric cell.
_MISSING = {"", "-", "--", ".", "...", "…", "n.a.", "na", "n/a", "*", "x", "X"}


@transient_retry()
def _fetch(code: str) -> dict:
    resp = get(DATA_URL, params={"FileName": code}, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _parse_value(cell):
    if cell is None:
        return None
    s = str(cell).strip().replace(",", "")
    if s in _MISSING:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_date(period: str):
    """Normalize a CBC period label to an ISO start-of-period date.

    Handles daily (YYYYMMDD), monthly (YYYYMmm), quarterly (YYYYQq) and annual
    (YYYY). Returns None for anything else so the row is kept but undated."""
    p = period.strip()
    m = re.fullmatch(r"(\d{4})(\d{2})(\d{2})", p)        # daily 20260601
    if m:
        yi, mo, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
        # Daily files carry two source conventions beyond plain calendar days:
        #   - month/period aggregates with month or day == 00 (e.g. 20131100 =
        #     the Nov-2013 average) -> snap to start-of-period.
        #   - a month-end marker that always uses day 31 (e.g. 20260431, the last
        #     April-2026 obs) -> clamp to the real last day of that month.
        # Either way we return a valid, sortable calendar date; the `period`
        # column preserves the source label so aggregates stay distinguishable.
        if not 1 <= mo <= 12:
            return f"{yi:04d}-01-01" if mo == 0 else None
        if day == 0:
            return f"{yi:04d}-{mo:02d}-01"
        last = calendar.monthrange(yi, mo)[1]
        day = min(day, last)
        return f"{yi:04d}-{mo:02d}-{day:02d}"
    m = re.fullmatch(r"(\d{4})M(\d{2})", p)               # monthly 1987M05
    if m:
        mo = int(m.group(2))
        if not 1 <= mo <= 12:
            return None
        return f"{m.group(1)}-{mo:02d}-01"
    m = re.fullmatch(r"(\d{4})Q([1-4])", p)               # quarterly 1984Q1
    if m:
        month = (int(m.group(2)) - 1) * 3 + 1
        return f"{m.group(1)}-{month:02d}-01"
    m = re.fullmatch(r"(\d{4})", p)                        # annual 1987
    if m:
        return f"{m.group(1)}-01-01"
    return None


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    code = CODE_BY_SPEC[node_id]
    payload = _fetch(code)
    data = payload["data"]
    dataSets = data["dataSets"]
    structure = data["structure"]

    # Dimension tables in numeric order (Table1 outermost). The value columns
    # of each row are the cartesian product of these member-label lists.
    tables = sorted(structure, key=lambda k: int(k.replace("Table", "")))
    dims = [[str(m["data"]).strip() for m in structure[t]] for t in tables]
    series_labels = [" | ".join(combo) for combo in itertools.product(*dims)]
    n_series = len(series_labels)

    periods, dates, series_col, values = [], [], [], []
    for row in dataSets:
        period = str(row[0]).strip()
        cells = row[1:]
        if len(cells) != n_series:
            raise AssertionError(
                f"{code}: row has {len(cells)} value cells but structure "
                f"implies {n_series} series (period {period})")
        iso = _parse_date(period)
        for label, cell in zip(series_labels, cells):
            periods.append(period)
            dates.append(iso)
            series_col.append(label)
            values.append(_parse_value(cell))

    table = pa.table(
        {"period": periods, "date": dates, "series": series_col, "value": values},
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# One published Delta table per matrix: cast the normalized date, keep only
# rows that carry an actual numeric value, and dedup on (period, series).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                period,
                CAST(date AS DATE) AS date,
                series,
                value
            FROM "{s.id}"
            WHERE value IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY period, series ORDER BY value
            ) = 1
        ''',
    )
    for s in DOWNLOAD_SPECS
]
