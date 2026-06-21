"""European Energy Crisis Fiscal Response Tracker — single Excel workbook
("Measures" sheet) of national fiscal measures responding to the energy crisis."""
import io

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import get_bytes, records, run_download, xlsx_link

EID = "2026-european-energy-crisis-fiscal-response-tracker"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/dataset/2026-european-energy-crisis-fiscal-response-tracker"


def parse(links):
    df = pd.read_excel(io.BytesIO(get_bytes(xlsx_link(links))),
                       sheet_name="Measures", header=0).dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return records(df)


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT
            "Country"                                        AS country,
            TRY_CAST("Date Announced" AS DATE)               AS date_announced,
            "Time Horizon"                                   AS time_horizon,
            "Status"                                         AS status,
            "Measure Name"                                   AS measure_name,
            "Details"                                        AS details,
            "Broad Measure Type"                             AS broad_measure_type,
            "Specific Measure Type"                          AS specific_measure_type,
            "Energy carrier"                                 AS energy_carrier,
            "Target Group"                                   AS target_group,
            TRY_CAST("Total Amount (in billion euros)" AS DOUBLE)  AS total_amount_billion_eur,
            TRY_CAST("GDP (in billion euros)" AS DOUBLE)           AS gdp_billion_eur,
            TRY_CAST("Measure in % of GDP" AS DOUBLE)              AS measure_pct_gdp
        FROM "{dep}"
        WHERE "Country" IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
