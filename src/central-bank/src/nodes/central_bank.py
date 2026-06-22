"""Central Bank of Taiwan (CBC) statistical database connector.

Mechanism `dataapi`: a custom stateless JSON API over the CBC PX-Web statistical
database. Each catalog entity is one PC-Axis (.px) file; we fetch its full
history in one request:

    GET https://cpx.cbc.gov.tw/api/dataapi/Get?FileName=<px_basename>
    -> {meta: {title, units, last_updated, matrix, ...},
        data: {dataSets: [[period, v1, v2, ...], ...],
               structure: {Table1: [{data: label}, ...], Table2: [...], ...}}}

`data.dataSets` row[0] is the time-period code (AD/Gregorian: 'YYYY' annual,
'YYYYMmm' monthly e.g. '1987M05', 'YYYYQn' quarterly, 'YYYYMMDD' daily). The
remaining values map 1:1 to the cross-product of the column dimensions in
`data.structure`, in `itertools.product(Table1, Table2, ...)` order (verified
against known magnitudes: M2 period-end ~= NT$69.5tn, NTD/USD ~= 31.5).

Each cube is a distinct schema, so we normalise every table to one uniform
LONG-format raw asset: (period, date, series, series_index, value). The
per-table SQL transform then casts value to DOUBLE and drops missing cells.

Strategy: stateless full re-pull. The corpus is small (~196 tables, tens of MB)
and the API exposes no incremental filter, so each refresh re-fetches the whole
table and overwrites. Freshness gating is the maintain step's job.
"""

from itertools import product

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import ENTITY_IDS

BASE = "https://cpx.cbc.gov.tw/api/dataapi/Get"

# Uniform long-format raw schema, identical for every .px table.
SCHEMA = pa.schema([
    ("period", pa.string()),         # raw source period code, e.g. '1987M05'
    ("date", pa.string()),           # parsed ISO date 'YYYY-MM-DD' or null
    ("series", pa.string()),         # cross-product label of the cube's column dims
    ("series_index", pa.int32()),    # 0-based column position within the row
    ("value", pa.string()),          # verbatim cell text (incl. missing markers)
])


def _node_id(entity_id: str) -> str:
    return f"central-bank-{entity_id.lower().replace('_', '-')}"


# Reverse map node-id -> original (case-sensitive) .px basename. Pure derived
# data, no I/O — mirrors the DOWNLOAD_SPECS comprehension below.
_PX_BY_NODE = {_node_id(e): e for e in ENTITY_IDS}


def _parse_period(p: str):
    """Map a CBC period code to an ISO date string, or None if unrecognised.

    Years are Gregorian (AD), not ROC. Periods are normalised to the first day
    of their interval (month/quarter/year start); daily codes are exact.
    """
    p = (p or "").strip()
    if not p:
        return None
    if p.isdigit():
        if len(p) == 4:                       # annual 'YYYY'
            return f"{p}-01-01"
        if len(p) == 8:                       # daily 'YYYYMMDD'
            return f"{p[0:4]}-{p[4:6]}-{p[6:8]}"
        return None
    if "M" in p:                              # monthly 'YYYYMmm'
        y, _, m = p.partition("M")
        if y.isdigit() and m.isdigit():
            mm = int(m)
            if 1 <= mm <= 12:
                return f"{int(y):04d}-{mm:02d}-01"
        return None
    if "Q" in p:                              # quarterly 'YYYYQn'
        y, _, q = p.partition("Q")
        if y.isdigit() and q.isdigit():
            qq = int(q)
            if 1 <= qq <= 4:
                return f"{int(y):04d}-{(qq - 1) * 3 + 1:02d}-01"
        return None
    return None


@transient_retry()
def _fetch(px_basename: str) -> dict:
    resp = get(BASE, params={"FileName": px_basename}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _column_labels(structure: dict) -> list:
    """Cross-product labels for the cube's value columns, in dataSets order."""
    dims = [[str(x.get("data")) for x in v]
            for v in structure.values() if isinstance(v, list) and v]
    if not dims:
        return []
    return [" | ".join(combo) for combo in product(*dims)]


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    px = _PX_BY_NODE[node_id]
    doc = _fetch(px)
    data = doc.get("data") or {}
    rows = data.get("dataSets") or []
    labels = _column_labels(data.get("structure") or {})

    periods, dates, series, indices, values = [], [], [], [], []
    for row in rows:
        if not row:
            continue
        period = str(row[0])
        iso = _parse_period(period)
        for i, cell in enumerate(row[1:]):
            periods.append(period)
            dates.append(iso)
            series.append(labels[i] if i < len(labels) else f"col_{i}")
            indices.append(i)
            values.append(None if cell is None else str(cell))

    table = pa.table(
        {
            "period": periods,
            "date": dates,
            "series": series,
            "series_index": indices,
            "value": values,
        },
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# One published Delta table per .px cube. Thin parse-and-type pass: cast the
# verbatim cell text to DOUBLE (dropping missing markers like '-'/'...'), keep
# only rows with a parseable date and a numeric value.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(date AS DATE)                            AS date,
                period,
                series,
                series_index,
                TRY_CAST(replace(value, ',', '') AS DOUBLE)   AS value
            FROM "{s.id}"
            WHERE date IS NOT NULL
              AND TRY_CAST(replace(value, ',', '') AS DOUBLE) IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
