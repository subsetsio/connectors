"""ATSIX — Aruoba Term Structure of Inflation Expectations."""

import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _read_xlsx, _write, _ymd

_ATSIX_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("horizon_months", pa.int64()),
    ("expected_inflation", pa.float64()),
])


def fetch_atsix(node_id: str) -> None:
    import pandas as pd
    url = f"{SND}/atsix/ATSIX_Vintages.xlsx"
    xl = _read_xlsx(_fetch_bytes(url))
    df = xl.parse(sheet_name="InfExp")
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
            hm = re.search(r"(\d+)$", str(c))
            if not hm:
                continue
            rows.append({
                "date": d, "horizon_months": int(hm.group(1)),
                "expected_inflation": float(v),
            })
    _write(rows, _ATSIX_SCHEMA, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-atsix", fn=fetch_atsix, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-atsix-transform",
        deps=["philadelphia-fed-atsix"],
        sql='''
            SELECT CAST(date AS DATE) AS date,
                   horizon_months,
                   expected_inflation
            FROM "philadelphia-fed-atsix"
            WHERE expected_inflation IS NOT NULL
            ORDER BY date, horizon_months
        ''',
    ),
]
