"""European Natural Gas Imports — ZIP of daily-flow CSVs; the daily_data CSV is
melted to long (date, source, flow in GWh/day)."""
import io
import zipfile

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import get_bytes, records, run_download

EID = "european-natural-gas-imports"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/dataset/european-natural-gas-imports"


def parse(links):
    zf = zipfile.ZipFile(io.BytesIO(get_bytes(links[0])))
    name = [n for n in zf.namelist()
            if "daily_data" in n.lower() and n.lower().endswith(".csv")][0]
    df = pd.read_csv(io.BytesIO(zf.read(name)))
    df = df.rename(columns={df.columns[0]: "date"})
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce").dt.date.astype(str)
    long = df.melt(id_vars=["date"], var_name="source", value_name="flow_gwh_d")
    long = long.dropna(subset=["flow_gwh_d"])
    return records(long)


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT CAST(date AS DATE) AS date, source,
               CAST(flow_gwh_d AS DOUBLE) AS flow_gwh_d
        FROM "{dep}" WHERE flow_gwh_d IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
