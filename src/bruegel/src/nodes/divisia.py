"""Divisia Monetary Aggregates (Euro Area) — ZIP with an Excel workbook ("Data"
sheet) of merged category/subcategory headers + series codes, flattened to long."""
import io
import re
import zipfile

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import clean, get_bytes, run_download

EID = "divisia-monetary-aggregates-euro-area"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/dataset/divisia-monetary-aggregates-euro-area"


def parse(links):
    zf = zipfile.ZipFile(io.BytesIO(get_bytes(links[0])))
    name = [n for n in zf.namelist() if n.lower().endswith((".xls", ".xlsx"))][0]
    raw = pd.read_excel(io.BytesIO(zf.read(name)), sheet_name="Data", header=None)
    cat = raw.iloc[1].ffill()       # merged category headers
    subcat = raw.iloc[2].ffill()    # merged subcategory text
    codes = raw.iloc[3]             # unique series codes
    out = []
    for _, row in raw.iloc[4:].iterrows():
        m = re.match(r"^(\d{4})M(\d{2})$", str(row.iloc[0]).strip())
        if not m:
            continue
        d = f"{m.group(1)}-{m.group(2)}-01"
        for ci in range(1, raw.shape[1]):
            code = codes.iloc[ci]
            val = row.iloc[ci]
            if pd.isna(code) or pd.isna(val):
                continue
            out.append({"date": d, "series_name": str(code).strip(),
                        "category": clean(cat.iloc[ci]),
                        "subcategory": clean(subcat.iloc[ci]),
                        "value": float(val)})
    return out


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT CAST(date AS DATE) AS date, series_name, category, subcategory,
               CAST(value AS DOUBLE) AS value
        FROM "{dep}" WHERE value IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
