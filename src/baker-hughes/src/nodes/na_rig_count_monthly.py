"""Baker Hughes — North America monthly rig count (current report).

Discovers the most-recently-dated 'North America Rig Count Report' file on the
/na-rig-count listing page and parses the long-format 'NAM Monthly' sheet. Stateless
full re-pull every run; the transform is a thin cast/projection over parquet.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, configure_http, save_raw_parquet

from utils import (
    NA_PAGE, UA, NA_DIMS,
    discover, download, pick_na_current, parse_na_long,
)

NA_MONTHLY_SCHEMA = pa.schema(NA_DIMS + [("rig_count", pa.float64())])


def fetch_na_monthly(node_id: str) -> None:
    configure_http(headers={"User-Agent": UA})
    uuid = pick_na_current(discover(NA_PAGE))
    rows = parse_na_long(download(uuid), "NAM Monthly", weekly=False)
    if not rows:
        raise RuntimeError("NAM Monthly produced 0 rows")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=NA_MONTHLY_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="baker-hughes-na-rig-count-monthly", fn=fetch_na_monthly, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="baker-hughes-na-rig-count-monthly-transform",
        deps=["baker-hughes-na-rig-count-monthly"],
        sql='''
            SELECT DISTINCT
                make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
                country, county, basin, gom, drill_for, location,
                state_province, trajectory,
                CAST(rig_count AS DOUBLE)    AS rig_count
            FROM "baker-hughes-na-rig-count-monthly"
            WHERE year IS NOT NULL AND month IS NOT NULL AND rig_count IS NOT NULL
        ''',
    ),
]
