"""SPF — Survey of Professional Forecasters consensus forecasts."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _read_xlsx, _write

_SPF_FILES = {
    ("mean", "level"): f"{SND}/survey-of-professional-forecasters/historical-data/meanLevel.xlsx",
    ("mean", "growth"): f"{SND}/survey-of-professional-forecasters/historical-data/meanGrowth.xlsx",
    ("median", "level"): f"{SND}/survey-of-professional-forecasters/historical-data/medianLevel.xlsx",
    ("median", "growth"): f"{SND}/survey-of-professional-forecasters/historical-data/medianGrowth.xlsx",
}
_SPF_HORIZON = {"1": "Q0", "2": "Q+1", "3": "Q+2", "4": "Q+3", "5": "Q+4",
                "6": "Q+5", "A": "annual_current", "B": "annual_next"}
_SPF_SCHEMA = pa.schema([
    ("survey_date", pa.string()),
    ("variable", pa.string()),
    ("horizon", pa.string()),
    ("statistic", pa.string()),
    ("measure", pa.string()),
    ("value", pa.float64()),
])


def fetch_spf_consensus(node_id: str) -> None:
    import pandas as pd
    rows = []
    for (statistic, measure), url in _SPF_FILES.items():
        xl = _read_xlsx(_fetch_bytes(url))
        for sheet in xl.sheet_names:
            df = xl.parse(sheet_name=sheet)
            cols = {str(c).strip().upper(): c for c in df.columns}
            if "YEAR" not in cols or "QUARTER" not in cols:
                continue
            variable = str(sheet).strip().upper()
            value_cols = [c for c in df.columns if str(c).strip().upper() not in ("YEAR", "QUARTER")]
            for _, r in df.iterrows():
                yr, q = r[cols["YEAR"]], r[cols["QUARTER"]]
                if pd.isna(yr) or pd.isna(q):
                    continue
                survey_date = f"{int(yr)}-Q{int(q)}"
                for c in value_cols:
                    v = r[c]
                    if pd.isna(v):
                        continue
                    horizon = _SPF_HORIZON.get(str(c).strip()[-1].upper())
                    if horizon is None:
                        continue
                    rows.append({
                        "survey_date": survey_date, "variable": variable,
                        "horizon": horizon, "statistic": statistic,
                        "measure": measure, "value": float(v),
                    })
    _write(rows, _SPF_SCHEMA, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-spf-consensus", fn=fetch_spf_consensus, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-spf-consensus-transform",
        deps=["philadelphia-fed-spf-consensus"],
        sql='''
            SELECT survey_date, variable, horizon, statistic, measure, value
            FROM "philadelphia-fed-spf-consensus"
            WHERE value IS NOT NULL
            ORDER BY survey_date, variable, horizon, statistic, measure
        ''',
    ),
]
