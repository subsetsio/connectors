"""Baker Hughes — North America weekly rig count (current report).

Discovers the most-recently-dated 'North America Rig Count Report' file on the
/na-rig-count listing page and parses the long-format 'NAM Weekly' sheet. Stateless
full re-pull every run; the transform is a thin cast/projection over parquet.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, configure_http, save_raw_parquet

from utils import (
    NA_PAGE, UA, NA_DIMS,
    discover, download, pick_na_current, parse_na_long,
)

NA_WEEKLY_SCHEMA = pa.schema(NA_DIMS + [("publish_date", pa.string()), ("rig_count", pa.float64())])


def fetch_na_weekly(node_id: str) -> None:
    configure_http(headers={"User-Agent": UA})
    uuid = pick_na_current(discover(NA_PAGE))
    rows = parse_na_long(download(uuid), "NAM Weekly", weekly=True)
    if not rows:
        raise RuntimeError("NAM Weekly produced 0 rows")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=NA_WEEKLY_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="baker-hughes-na-rig-count-weekly", fn=fetch_na_weekly, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="baker-hughes-na-rig-count-weekly-transform",
        deps=["baker-hughes-na-rig-count-weekly"],
        sql='''
            SELECT DISTINCT
                CAST(publish_date AS DATE)   AS date,
                country, county, basin, gom, drill_for, location,
                state_province, trajectory,
                CAST(rig_count AS INTEGER)   AS rig_count
            FROM "baker-hughes-na-rig-count-weekly"
            WHERE publish_date IS NOT NULL AND rig_count IS NOT NULL
        ''',
    ),
]
