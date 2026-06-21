"""GSoD Indices — the Global State of Democracy Indices country-year panel.

GET /gsod-indices/api/data?year1=&year2= returns the whole panel as a JSON
array of country-year rows (~9000 rows x 86 columns; string-encoded floats).
One request is the bulk export; we pass a wide year window so the API hands
back every year it has (currently 1975-2021).
"""

from datetime import datetime, timezone

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import GSOD_API, request


def fetch_gsod_indices(node_id: str) -> None:
    asset = node_id
    # Pass a wide window so the API returns every year it holds. year1/year2 are
    # required; a literal floor of 1900 plus "next year" discovers the period set
    # rather than hardcoding a range loop.
    year2 = datetime.now(tz=timezone.utc).year + 1
    resp = request(f"{GSOD_API}/data", params={"year1": 1900, "year2": year2})
    rows = resp.json()
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"GSoD /api/data returned no rows: {str(rows)[:200]}")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="international-idea-gsod-indices", fn=fetch_gsod_indices, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="international-idea-gsod-indices-transform",
        deps=["international-idea-gsod-indices"],
        sql='''
            SELECT
                CAST(ID_country_code AS INTEGER)   AS country_code,
                ID_country_name                    AS country_name,
                CAST(ID_year AS INTEGER)           AS year,
                TRY_CAST(ID_region AS INTEGER)     AS region_id,
                TRY_CAST(ID_subregion AS INTEGER)  AS subregion_id,
                TRY_CAST(dem AS INTEGER)           AS dem_performance_band,
                TRY_CAST(demperf AS INTEGER)       AS dem_performance,
                TRY_CAST(COLUMNS('^(A|SA|SC)_') AS DOUBLE)
            FROM "international-idea-gsod-indices"
            WHERE ID_year IS NOT NULL AND ID_country_code IS NOT NULL
        ''',
    ),
]
