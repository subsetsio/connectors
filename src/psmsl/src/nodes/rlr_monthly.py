"""PSMSL Revised Local Reference monthly mean sea level (datum-controlled)."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import MONTHLY_SCHEMA, MONTHLY_SQL, RLR_MONTHLY_ZIP, download_zip, parse_monthly


def fetch_rlr_monthly(node_id: str) -> None:
    asset = node_id
    zf = download_zip(RLR_MONTHLY_ZIP)
    rows = parse_monthly(zf, ".rlrdata")
    table = pa.Table.from_pylist(rows, schema=MONTHLY_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="psmsl-rlr-monthly", fn=fetch_rlr_monthly, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="psmsl-rlr-monthly-transform",
        deps=["psmsl-rlr-monthly"],
        sql=MONTHLY_SQL.format(dep="psmsl-rlr-monthly"),
    ),
]
