"""US Foreign Military Sales — single Excel workbook ("MAINDATA" sheet) of
announced US arms sales by country, equipment and contractor."""
import io

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import get_bytes, records, run_download, xlsx_link

EID = "us-foreign-military-sales"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/dataset/us-foreign-military-sales"


def parse(links):
    df = pd.read_excel(io.BytesIO(get_bytes(xlsx_link(links))),
                       sheet_name="MAINDATA", header=0).dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return records(df)


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT
            TRY_CAST(id AS INTEGER)               AS id,
            country,
            TRY_CAST(financial_value AS DOUBLE)   AS financial_value_bn_usd,
            main_equipment,
            military_domain,
            general_item_type,
            specific_item_type,
            contractors,
            TRY_CAST(year AS INTEGER)             AS year,
            TRY_CAST(month AS INTEGER)            AS month
        FROM "{dep}" WHERE country IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
