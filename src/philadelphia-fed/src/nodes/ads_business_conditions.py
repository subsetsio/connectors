"""ADS — Aruoba-Diebold-Scotti Business Conditions Index (daily)."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _read_xlsx, _write

_ADS_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("ads_index", pa.float64()),
    ("recession_bar", pa.float64()),
])


def fetch_ads_business_conditions(node_id: str) -> None:
    import pandas as pd
    url = f"{SND}/ads/ADS_Index_Most_Current_Vintage.xlsx"
    xl = _read_xlsx(_fetch_bytes(url))
    df = xl.parse(sheet_name=xl.sheet_names[0])
    df.columns = [str(c).strip() for c in df.columns]
    rows = []
    for _, r in df.iterrows():
        d, v = r.get("Date"), r.get("ADS_Index")
        if pd.isna(d) or pd.isna(v):
            continue
        # Date arrives as 'YYYY:MM:DD'
        ds = str(d).strip().replace(":", "-")
        rec = r.get("RECBARS")
        rows.append({
            "date": ds, "ads_index": float(v),
            "recession_bar": None if pd.isna(rec) else float(rec),
        })
    _write(rows, _ADS_SCHEMA, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-ads-business-conditions", fn=fetch_ads_business_conditions, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-ads-business-conditions-transform",
        deps=["philadelphia-fed-ads-business-conditions"],
        sql='''
            SELECT CAST(date AS DATE) AS date,
                   ads_index,
                   recession_bar
            FROM "philadelphia-fed-ads-business-conditions"
            WHERE ads_index IS NOT NULL
            ORDER BY date
        ''',
    ),
]
