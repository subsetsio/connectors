"""Real Effective Exchange Rates for 178 countries — ZIP with an Excel workbook
whose sheets (REER/NEER x MONTHLY/ANNUAL x country-set) are flattened to long."""
import io
import re
import zipfile

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import clean, get_bytes, run_download

EID = "real-effective-exchange-rates-for-178-countries-a-new-database"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/publications/datasets/real-effective-exchange-rates-for-178-countries-a-new-database"


def parse(links):
    zf = zipfile.ZipFile(io.BytesIO(get_bytes(links[0])))
    name = [n for n in zf.namelist() if n.lower().endswith((".xls", ".xlsx"))][0]
    xl = pd.ExcelFile(io.BytesIO(zf.read(name)))
    out = []
    for sh in xl.sheet_names:
        m = re.match(r"(REER|NEER)_(MONTHLY|ANNUAL)_(\d+)$", sh.strip())
        if not m:
            continue
        measure, freq, cset = m.group(1), m.group(2).lower(), m.group(3)
        raw = xl.parse(sh, header=None)
        codes = raw.iloc[0]
        for _, r in raw.iloc[1:].iterrows():
            period = r.iloc[0]
            if pd.isna(period):
                continue
            period = str(period).strip()
            for j in range(1, raw.shape[1]):
                val = r.iloc[j]
                if pd.isna(val):
                    continue
                code = str(codes.iloc[j]).strip()
                cc = code.split("_")[-1] if "_" in code else code
                out.append({"period": period, "measure": measure, "frequency": freq,
                            "country_set": cset, "country_code": cc, "value": clean(val)})
    return out


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT period, measure, frequency, country_set, country_code,
               CAST(value AS DOUBLE) AS value
        FROM "{dep}" WHERE value IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
