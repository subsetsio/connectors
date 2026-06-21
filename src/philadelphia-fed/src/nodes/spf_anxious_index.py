"""SPF — Anxious Index (probability of decline in real GDP)."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _read_xlsx, _write

_ANXIOUS_SCHEMA = pa.schema([
    ("survey_date", pa.string()),
    ("anxious_index", pa.float64()),
    ("recession", pa.float64()),
])


def fetch_spf_anxious_index(node_id: str) -> None:
    import pandas as pd
    url = f"{SND}/survey-of-professional-forecasters/anxious-index/anxious_index_chart.xlsx"
    xl = _read_xlsx(_fetch_bytes(url))
    # header block: real columns (Obs Year, Obs Quarter, Anxious Index, RECESS) at row 3
    df = xl.parse(sheet_name="Data", skiprows=3)
    df.columns = [str(c).strip() for c in df.columns]
    rows = []
    for _, r in df.iterrows():
        yr, q, idx = r.get("Obs Year"), r.get("Obs Quarter"), r.get("Anxious Index")
        if pd.isna(yr) or pd.isna(q) or pd.isna(idx):
            continue
        rec = r.get("RECESS")
        rows.append({
            "survey_date": f"{int(yr)}-Q{int(q)}",
            "anxious_index": float(idx),
            "recession": None if pd.isna(rec) else float(rec),
        })
    _write(rows, _ANXIOUS_SCHEMA, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-spf-anxious-index", fn=fetch_spf_anxious_index, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-spf-anxious-index-transform",
        deps=["philadelphia-fed-spf-anxious-index"],
        # `recession` is dropped: the source RECESS column carries a 99999 sentinel
        # for "missing" plus blanks — no real signal, so we publish only the index.
        sql='''
            SELECT survey_date, anxious_index
            FROM "philadelphia-fed-spf-anxious-index"
            WHERE anxious_index IS NOT NULL
            ORDER BY survey_date
        ''',
    ),
]
