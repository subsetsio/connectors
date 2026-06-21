"""Livingston Survey — consensus mean forecasts."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _read_xlsx, _write, _ymd

_LIVINGSTON_SCHEMA = pa.schema([
    ("survey_date", pa.string()),
    ("variable", pa.string()),
    ("horizon", pa.string()),
    ("value", pa.float64()),
])


def fetch_livingston_survey(node_id: str) -> None:
    import pandas as pd
    url = f"{SND}/livingston-survey/historical-data/means.xlsx"
    xl = _read_xlsx(_fetch_bytes(url))
    rows = []
    for sheet in xl.sheet_names:
        df = xl.parse(sheet_name=sheet)
        cols = {str(c).strip().lower(): c for c in df.columns}
        if "date" not in cols:
            continue
        variable = str(sheet).strip().upper()
        date_col = cols["date"]
        value_cols = [c for c in df.columns if c != date_col]
        for _, r in df.iterrows():
            d = _ymd(r[date_col])
            if d is None:
                continue
            for c in value_cols:
                v = r[c]
                if pd.isna(v):
                    continue
                name = str(c).strip()
                # column 'RGDPX_6M' -> horizon '6M'
                horizon = name.split("_", 1)[1] if "_" in name else name
                rows.append({
                    "survey_date": d, "variable": variable,
                    "horizon": horizon.upper(), "value": float(v),
                })
    _write(rows, _LIVINGSTON_SCHEMA, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-livingston-survey", fn=fetch_livingston_survey, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-livingston-survey-transform",
        deps=["philadelphia-fed-livingston-survey"],
        sql='''
            SELECT CAST(survey_date AS DATE) AS survey_date,
                   variable, horizon, value
            FROM "philadelphia-fed-livingston-survey"
            WHERE value IS NOT NULL
            ORDER BY survey_date, variable, horizon
        ''',
    ),
]
