"""IDMC displacements — GIDD combined conflict+disaster totals, per country-year (~2.3k)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import fetch_gidd


def fetch_displacements(node_id: str) -> None:
    save_raw_ndjson(fetch_gidd("displacements"), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="idmc-displacements", fn=fetch_displacements, kind="download"),
]

_SQL_DISPLACEMENTS = """
SELECT
    iso3,
    country_name,
    CAST(year AS INTEGER) AS year,
    CAST(conflict_new_displacement AS BIGINT) AS conflict_new_displacement,
    CAST(conflict_new_displacement_rounded AS BIGINT) AS conflict_new_displacement_rounded,
    CAST(conflict_total_displacement AS BIGINT) AS conflict_total_displacement,
    CAST(conflict_total_displacement_rounded AS BIGINT) AS conflict_total_displacement_rounded,
    CAST(disaster_new_displacement AS BIGINT) AS disaster_new_displacement,
    CAST(disaster_new_displacement_rounded AS BIGINT) AS disaster_new_displacement_rounded,
    CAST(disaster_total_displacement AS BIGINT) AS disaster_total_displacement,
    CAST(disaster_total_displacement_rounded AS BIGINT) AS disaster_total_displacement_rounded
FROM "idmc-displacements"
WHERE iso3 IS NOT NULL AND year IS NOT NULL
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(id="idmc-displacements-transform", deps=["idmc-displacements"], sql=_SQL_DISPLACEMENTS),
]
