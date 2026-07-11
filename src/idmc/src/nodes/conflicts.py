"""IDMC conflicts — GIDD conflict/violence figures, per country-year (~1019 rows)."""

from subsets_utils import save_raw_ndjson
from utils import fetch_gidd


def fetch_conflicts(node_id: str) -> None:
    save_raw_ndjson(fetch_gidd("conflicts"), node_id)


_SQL_CONFLICTS = """
SELECT
    iso3,
    country_name,
    CAST(year AS INTEGER) AS year,
    CAST(new_displacement AS BIGINT) AS new_displacement,
    CAST(new_displacement_rounded AS BIGINT) AS new_displacement_rounded,
    CAST(total_displacement AS BIGINT) AS total_displacement,
    CAST(total_displacement_rounded AS BIGINT) AS total_displacement_rounded
FROM "idmc-conflicts"
WHERE iso3 IS NOT NULL AND year IS NOT NULL
"""
