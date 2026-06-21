"""PSMSL Metric monthly mean sea level (legacy, no datum control)."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import MET_MONTHLY_ZIP, MONTHLY_SCHEMA, MONTHLY_SQL, download_zip, parse_monthly


def fetch_met_monthly(node_id: str) -> None:
    asset = node_id
    zf = download_zip(MET_MONTHLY_ZIP)
    rows = parse_monthly(zf, ".metdata")
    table = pa.Table.from_pylist(rows, schema=MONTHLY_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="psmsl-met-monthly", fn=fetch_met_monthly, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="psmsl-met-monthly-transform",
        deps=["psmsl-met-monthly"],
        sql=MONTHLY_SQL.format(dep="psmsl-met-monthly"),
    ),
]
