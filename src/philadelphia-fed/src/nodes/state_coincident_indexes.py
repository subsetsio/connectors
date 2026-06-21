"""State Coincident Indexes (50 states + US, monthly)."""

import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _write, _ymd

_COINCIDENT_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("state", pa.string()),
    ("coincident_index", pa.float64()),
])


def fetch_state_coincident_indexes(node_id: str) -> None:
    import pandas as pd
    url = f"{SND}/coincident/coincident-revised.xls"
    # .xls (legacy BIFF) — read with xlrd; the core.xml date bug is xlsx-only.
    xl = pd.ExcelFile(io.BytesIO(_fetch_bytes(url)), engine="xlrd")
    df = xl.parse(sheet_name="Indexes")
    df.columns = [str(c).strip() for c in df.columns]
    date_col = df.columns[0]
    rows = []
    for _, r in df.iterrows():
        d = _ymd(r[date_col])
        if d is None:
            continue
        for c in df.columns[1:]:
            v = r[c]
            if pd.isna(v):
                continue
            rows.append({"date": d, "state": str(c).strip().upper(), "coincident_index": float(v)})
    _write(rows, _COINCIDENT_SCHEMA, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-state-coincident-indexes", fn=fetch_state_coincident_indexes, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-state-coincident-indexes-transform",
        deps=["philadelphia-fed-state-coincident-indexes"],
        sql='''
            SELECT CAST(date AS DATE) AS date,
                   state,
                   coincident_index
            FROM "philadelphia-fed-state-coincident-indexes"
            WHERE coincident_index IS NOT NULL
            ORDER BY date, state
        ''',
    ),
]
