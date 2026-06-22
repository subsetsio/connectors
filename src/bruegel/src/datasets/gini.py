"""Global and Regional Gini Coefficients — ZIP containing an Excel workbook
("Database" sheet, wide by year) melted to long (group/method/year, gini)."""
import io
import zipfile

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import get_bytes, records, run_download

EID = "global-and-regional-gini-coefficients-income-inequality"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/dataset/global-and-regional-gini-coefficients-income-inequality"

# The live file is under /system/files/, which the apex host 302s back to the
# CI-blocked www. No mirror exists, but the Wayback Machine (CI-reachable) holds
# the last archived edition — the ZIP/.xls "Database" sheet is structurally
# identical, just a refresh or two behind. Used via run_download(direct_links=).
FILE_URL = ("https://web.archive.org/web/20230219115914id_/"
            "https://www.bruegel.org/sites/default/files/2023-01/"
            "Global_income_inequality_database_ver_13Jan2023.zip")


def parse(links):
    zf = zipfile.ZipFile(io.BytesIO(get_bytes(links[0])))
    name = [n for n in zf.namelist() if n.lower().endswith((".xls", ".xlsx"))][0]
    df = pd.read_excel(io.BytesIO(zf.read(name)), sheet_name="Database", header=0)
    id_cols = ["Type", "Mean income", "Method", "Group", "Variable name"]
    year_cols = [c for c in df.columns
                 if isinstance(c, (int, float)) or str(c).strip().isdigit()]
    long = df.melt(id_vars=id_cols, value_vars=year_cols,
                   var_name="year", value_name="gini").dropna(subset=["gini"])
    long["year"] = long["year"].astype(float).astype(int)
    long = long.rename(columns={"Type": "income_type", "Mean income": "mean_income",
                                "Method": "method", "Group": "country_group",
                                "Variable name": "variable_name"})
    return records(long)


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT variable_name, income_type, mean_income, method,
               country_group, CAST(year AS INTEGER) AS year,
               CAST(gini AS DOUBLE) AS gini
        FROM "{dep}" WHERE gini IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
