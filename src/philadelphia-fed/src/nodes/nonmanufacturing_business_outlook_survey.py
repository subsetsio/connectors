"""Nonmanufacturing Business Outlook Survey (NBOS) — diffusion indexes."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _read_xlsx, _write, _ymd

_NBOS_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("indicator", pa.string()),
    ("diffusion_index", pa.float64()),
])


def fetch_nonmanufacturing_business_outlook_survey(node_id: str) -> None:
    import pandas as pd
    url = f"{SND}/NBOS/nboshistory.xlsx"
    xl = _read_xlsx(_fetch_bytes(url))
    df = xl.parse(sheet_name="Diffusion")
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
            rows.append({"date": d, "indicator": str(c).strip(), "diffusion_index": float(v)})
    _write(rows, _NBOS_SCHEMA, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-nonmanufacturing-business-outlook-survey", fn=fetch_nonmanufacturing_business_outlook_survey, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-nonmanufacturing-business-outlook-survey-transform",
        deps=["philadelphia-fed-nonmanufacturing-business-outlook-survey"],
        sql='''
            SELECT CAST(date AS DATE) AS date,
                   indicator,
                   diffusion_index
            FROM "philadelphia-fed-nonmanufacturing-business-outlook-survey"
            WHERE diffusion_index IS NOT NULL
            ORDER BY date, indicator
        ''',
    ),
]
