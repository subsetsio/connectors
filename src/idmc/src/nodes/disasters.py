"""IDMC disasters — GIDD disaster figures, per event = country-year-hazard (~29.7k)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import fetch_gidd, join_field


def fetch_disasters(node_id: str) -> None:
    rows = fetch_gidd("disasters")
    for r in rows:
        # event_codes / event_codes_type are arrays — flatten to scalar strings
        r["event_codes"] = join_field(r.get("event_codes"))
        r["event_codes_type"] = join_field(r.get("event_codes_type"))
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="idmc-disasters", fn=fetch_disasters, kind="download"),
]

_SQL_DISASTERS = """
SELECT
    iso3,
    country_name,
    CAST(year AS INTEGER) AS year,
    TRY_CAST(start_date AS DATE) AS start_date,
    start_date_accuracy,
    TRY_CAST(end_date AS DATE) AS end_date,
    end_date_accuracy,
    event_name,
    CAST(new_displacement AS BIGINT) AS new_displacement,
    CAST(new_displacement_rounded AS BIGINT) AS new_displacement_rounded,
    CAST(total_displacement AS BIGINT) AS total_displacement,
    CAST(total_displacement_rounded AS BIGINT) AS total_displacement_rounded,
    hazard_category_name,
    hazard_sub_category_name,
    hazard_type_name,
    hazard_sub_type_name,
    event_codes,
    event_codes_type
FROM "idmc-disasters"
WHERE iso3 IS NOT NULL AND year IS NOT NULL
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(id="idmc-disasters-transform", deps=["idmc-disasters"], sql=_SQL_DISASTERS),
]
