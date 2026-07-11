"""SPF - cross-sectional forecast dispersion."""

import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _read_xlsx, _write

_DISPERSION_SCHEMA = pa.schema([
    ("survey_date", pa.string()),
    ("variable", pa.string()),
    ("horizon", pa.string()),
    ("measure", pa.string()),
    ("value", pa.float64()),
])


def _horizon(label: str) -> str | None:
    m = re.search(r"\((T(?:\+\d+)?)\)$", label)
    if not m:
        return None
    return {"T": "Q0", "T+1": "Q+1", "T+2": "Q+2", "T+3": "Q+3", "T+4": "Q+4"}.get(m.group(1))


def _measure(label: str) -> str | None:
    u = label.upper()
    for token in ("P25", "P75", "D1"):
        if f"_{token}_" in u:
            return token.lower()
    return None


def fetch_spf_dispersion(node_id: str) -> None:
    import pandas as pd

    url = f"{SND}/survey-of-professional-forecasters/historical-data/Dispersion_1.xlsx"
    xl = _read_xlsx(_fetch_bytes(url))
    rows = []
    for sheet in xl.sheet_names:
        raw = xl.parse(sheet_name=sheet, header=None)
        header_idx = None
        for i in range(min(len(raw), 25)):
            if str(raw.iat[i, 0]).strip().lower() == "survey_date(t)":
                header_idx = i
                break
        if header_idx is None:
            continue
        headers = [str(v).strip() for v in raw.iloc[header_idx].tolist()]
        variable = str(sheet).strip().upper()
        data = raw.iloc[header_idx + 1:]
        for _, r in data.iterrows():
            survey_date = str(r.iloc[0]).strip()
            if not survey_date or survey_date.lower() == "nan":
                continue
            for idx, col in enumerate(headers[1:], start=1):
                measure = _measure(col)
                horizon = _horizon(col)
                if measure is None or horizon is None:
                    continue
                value = r.iloc[idx]
                if pd.isna(value):
                    continue
                rows.append({
                    "survey_date": survey_date.replace("Q", "-Q"),
                    "variable": variable,
                    "horizon": horizon,
                    "measure": measure,
                    "value": float(value),
                })
    _write(rows, _DISPERSION_SCHEMA, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-spf-dispersion", fn=fetch_spf_dispersion, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-spf-dispersion-transform",
        deps=["philadelphia-fed-spf-dispersion"],
        sql='''
            SELECT survey_date, variable, horizon, measure, value
            FROM "philadelphia-fed-spf-dispersion"
            WHERE value IS NOT NULL
            ORDER BY survey_date, variable, horizon, measure
        ''',
    ),
]
