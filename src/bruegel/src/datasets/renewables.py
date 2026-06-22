"""EU Renewables Value Tracker — single Excel workbook ("Data" sheet) of
capacity factor / market value / capture value by zone, year and technology."""
import io

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import get_bytes, records, run_download, xlsx_link

EID = "eu-renewables-value-tracker"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/dataset/eu-renewables-value-tracker"


def parse(links):
    df = pd.read_excel(io.BytesIO(get_bytes(xlsx_link(links))),
                       sheet_name="Data", header=0).dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    df["zone"] = df["zone"].astype(str).str.strip()
    return records(df)


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT zone, CAST(year AS INTEGER) AS year, tech,
               CAST(CF AS DOUBLE) AS capacity_factor,
               CAST(MV AS DOUBLE) AS market_value,
               CAST(CV AS DOUBLE) AS capture_value
        FROM "{dep}" WHERE CF IS NOT NULL OR MV IS NOT NULL OR CV IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
