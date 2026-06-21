"""national-highways-sites — reference register of ~20k sensor sites.

A single snapshot of the WebTRIS /sites endpoint (no per-site crawl).
"""

from __future__ import annotations

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _all_sites

_SITES_SCHEMA = pa.schema([
    ("site_id", pa.string()),
    ("name", pa.string()),
    ("description", pa.string()),
    ("longitude", pa.float64()),
    ("latitude", pa.float64()),
    ("status", pa.string()),
])


def fetch_sites(node_id: str) -> None:
    rows = _all_sites()
    table = pa.Table.from_pylist(
        [
            {
                "site_id": str(s.get("Id")),
                "name": s.get("Name"),
                "description": s.get("Description"),
                "longitude": s.get("Longitude"),
                "latitude": s.get("Latitude"),
                "status": s.get("Status"),
            }
            for s in rows
        ],
        schema=_SITES_SCHEMA,
    )
    save_raw_parquet(table, node_id)


_SITES_SQL = '''
    SELECT
        site_id,
        name,
        description,
        CAST(longitude AS DOUBLE) AS longitude,
        CAST(latitude  AS DOUBLE) AS latitude,
        status
    FROM "national-highways-sites"
    WHERE site_id IS NOT NULL
'''

DOWNLOAD_SPECS = [
    NodeSpec(id="national-highways-sites", fn=fetch_sites, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="national-highways-sites-transform",
        deps=["national-highways-sites"],
        sql=_SITES_SQL,
    ),
]
