"""Partisan Conflict Index."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import MEDIA, _fetch_bytes, _read_xlsx, _write

_MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], start=1)}

_PARTISAN_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("partisan_conflict_index", pa.float64()),
])


def fetch_partisan_conflict_index(node_id: str) -> None:
    import pandas as pd
    url = f"{MEDIA}/Data-Visualizations/partisan-conflict.xlsx"
    xl = _read_xlsx(_fetch_bytes(url))
    df = xl.parse(sheet_name="Sheet1")
    df.columns = [str(c).strip() for c in df.columns]
    rows = []
    for _, r in df.iterrows():
        yr, mon, val = r.get("Year"), r.get("Month"), r.get("Partisan Conflict")
        if pd.isna(yr) or pd.isna(mon) or pd.isna(val):
            continue
        mnum = _MONTHS.get(str(mon).strip().lower())
        if mnum is None:
            continue
        rows.append({
            "date": f"{int(yr):04d}-{mnum:02d}-01",
            "partisan_conflict_index": float(val),
        })
    _write(rows, _PARTISAN_SCHEMA, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-partisan-conflict-index", fn=fetch_partisan_conflict_index, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-partisan-conflict-index-transform",
        deps=["philadelphia-fed-partisan-conflict-index"],
        sql='''
            SELECT CAST(date AS DATE) AS date,
                   partisan_conflict_index
            FROM "philadelphia-fed-partisan-conflict-index"
            WHERE partisan_conflict_index IS NOT NULL
            ORDER BY date
        ''',
    ),
]
