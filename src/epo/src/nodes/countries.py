"""EPO country metadata (countries-metadata.json)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import fetch_json


def fetch_countries(node_id: str) -> None:
    """countries-metadata.json: a flat list of country records."""
    data = fetch_json("countries-metadata.json")
    save_raw_ndjson(data, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="epo-countries", fn=fetch_countries, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="epo-countries-transform",
        deps=["epo-countries"],
        sql='''
            SELECT
                CAST(county_id AS INTEGER)           AS country_id,
                country_code,
                country_name,
                CAST(country_ip5 AS INTEGER)         AS is_ip5,
                CAST(country_ue AS INTEGER)          AS is_eu,
                CAST(country_epo_member AS INTEGER)  AS is_epo_member,
                CAST(country_population AS BIGINT)   AS population
            FROM "epo-countries"
        ''',
    ),
]
