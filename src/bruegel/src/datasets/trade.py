"""Global Trade Tracker — multi-sheet Excel workbook (one sheet per commodity,
two header rows for flow/partner) flattened to long observations."""
import io

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import clean, get_bytes, run_download, xlsx_link

EID = "global-trade-tracker"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/dataset/global-trade-tracker"


def parse(links):
    xl = pd.ExcelFile(io.BytesIO(get_bytes(xlsx_link(links))))
    out = []
    for sh in xl.sheet_names:
        if sh.strip().upper().startswith("READ"):
            continue
        parts = [p.strip() for p in sh.split(",")]
        commodity = parts[0] if parts else sh
        unit = parts[1] if len(parts) > 1 else None
        sa = parts[2] if len(parts) > 2 else None
        raw = xl.parse(sh, header=None)
        flow_row = raw.iloc[0].ffill()
        country_row = raw.iloc[1]
        for _, r in raw.iloc[2:].iterrows():
            dt = r.iloc[0]
            if pd.isna(dt):
                continue
            d = pd.Timestamp(dt).date().isoformat()
            for j in range(1, raw.shape[1]):
                val = r.iloc[j]
                if pd.isna(val):
                    continue
                out.append({"date": d, "commodity": commodity, "unit": unit,
                            "seasonal_adj": sa, "flow": clean(flow_row.iloc[j]),
                            "partner": clean(country_row.iloc[j]), "value": clean(val)})
    return out


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT CAST(date AS DATE) AS date, commodity, unit, seasonal_adj,
               flow, partner, CAST(value AS DOUBLE) AS value
        FROM "{dep}" WHERE value IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
