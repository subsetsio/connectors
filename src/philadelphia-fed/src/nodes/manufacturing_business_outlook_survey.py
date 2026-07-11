"""Manufacturing Business Outlook Survey (MBOS) — diffusion indexes (CSV)."""

import datetime
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _write

_MBOS_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("indicator", pa.string()),
    ("diffusion_index", pa.float64()),
])


def _mon_yy(s: str) -> str | None:
    s = str(s).strip()
    try:
        dt = datetime.datetime.strptime(s, "%b-%y")
    except ValueError:
        return None
    year = dt.year
    if year > 2030:  # %y pivots at 1969; MBOS starts 1968 -> pull 20xx back to 19xx
        year -= 100
    return f"{year:04d}-{dt.month:02d}-01"


def fetch_manufacturing_business_outlook_survey(node_id: str) -> None:
    import pandas as pd
    url = f"{SND}/MBOS/Historical-Data/Diffusion-Indexes/bos_dif.csv"
    df = pd.read_csv(io.BytesIO(_fetch_bytes(url)))
    df.columns = [str(c).strip() for c in df.columns]
    date_col = df.columns[0]
    rows = []
    for _, r in df.iterrows():
        d = _mon_yy(r[date_col])
        if d is None:
            continue
        for c in df.columns[1:]:
            v = r[c]
            if pd.isna(v):
                continue
            rows.append({"date": d, "indicator": str(c).strip(), "diffusion_index": float(v)})
    _write(rows, _MBOS_SCHEMA, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-manufacturing-business-outlook-survey", fn=fetch_manufacturing_business_outlook_survey, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-manufacturing-business-outlook-survey-transform",
        deps=["philadelphia-fed-manufacturing-business-outlook-survey"],
        sql='''
            SELECT CAST(date AS DATE) AS date,
                   indicator,
                   diffusion_index
            FROM "philadelphia-fed-manufacturing-business-outlook-survey"
            WHERE diffusion_index IS NOT NULL
            ORDER BY date, indicator
        ''',
    ),
]
