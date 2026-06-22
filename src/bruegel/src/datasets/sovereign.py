"""Sovereign Bond Holdings — Excel workbook with cross-country QUARTERLY and
ANNUAL sheets (merged country/holder headers) flattened to long observations."""
import io
import re

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import get_bytes, run_download, xlsx_link

EID = "sovereign-bond-holdings"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/dataset/sovereign-bond-holdings"

# The live file is under /system/files/, which the apex host 302s back to the
# CI-blocked www. This is a static (2020) dataset, so the Wayback-archived copy
# (CI-reachable) IS the current file — same workbook, same cross-country sheets.
# Filename contains "dataset2", so parse()'s selector picks it unchanged.
FILE_URL = ("https://web.archive.org/web/20201030130126id_/"
            "https://www.bruegel.org/wp-content/uploads/2020/04/"
            "202004_Bruegel_sovereign_bond_-holding_dataset2.xlsx")


def parse(links):
    url = [u for u in links if "dataset2" in u.lower()] or [xlsx_link(links)]
    data = get_bytes(url[0])

    def parse_cross(sheet, freq):
        raw = pd.read_excel(io.BytesIO(data), sheet_name=sheet, header=None)
        countries = raw.iloc[1].ffill()
        holders = raw.iloc[2]
        recs = []
        for _, row in raw.iloc[3:].iterrows():
            dval = row.iloc[0]
            if isinstance(dval, str) or pd.isna(dval):
                continue  # skip footnote / blank rows
            if freq == "quarterly":
                date = pd.Timestamp(dval).date().isoformat()
            else:
                date = f"{int(dval)}-01-01"
            for ci in range(1, raw.shape[1]):
                ctry, hold = countries.iloc[ci], holders.iloc[ci]
                val = row.iloc[ci]
                if pd.isna(ctry) or pd.isna(hold) or pd.isna(val):
                    continue
                recs.append({"date": date, "country": str(ctry).strip(),
                             "holder_type": re.sub(r"\*+$", "", str(hold).strip()).strip(),
                             "value": float(val), "frequency": freq})
        return recs

    return parse_cross("cross countries QUARTERLY", "quarterly") + \
        parse_cross("cross countries ANNUAL", "annual")


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT CAST(date AS DATE) AS date, country, holder_type, frequency,
               CAST(value AS DOUBLE) AS value
        FROM "{dep}" WHERE value IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
