"""Global Lake & River Ice Phenology Database (NSIDC G01377).

The whole source is two stable, public CSV files under
https://noaadata.apps.nsidc.org/NOAA/G01377/ . Both are tiny (~3.2MB total),
so the fetch shape is the default stateless full re-pull: download each CSV in
full every run and overwrite. No incremental filter is exposed and none is
needed.

Raw is saved faithfully as NDJSON (every value a string, exactly as the CSV
delivers it); the missing-value sentinels the source uses (-999 for numerics,
'-' for text) are stripped and the columns typed in the transform SQL.
"""
import csv
import io

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://noaadata.apps.nsidc.org/NOAA/G01377"

CSV_URLS = {
    "lake-river-ice-phenology-freeze-thaw": f"{BASE}/liag_freeze_thaw_table.csv",
    "lake-river-ice-phenology-physical-characteristics": f"{BASE}/liag_physical_character_table.csv",
}


@transient_retry()
def _fetch_csv_rows(url: str) -> list[dict]:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    text = resp.content.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    return [dict(row) for row in reader]


def fetch_csv(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    url = CSV_URLS[node_id]
    rows = _fetch_csv_rows(url)
    if not rows:
        raise AssertionError(f"{node_id}: fetched 0 rows from {url}")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="lake-river-ice-phenology-freeze-thaw", fn=fetch_csv, kind="download"),
    NodeSpec(id="lake-river-ice-phenology-physical-characteristics", fn=fetch_csv, kind="download"),
]


# --- transforms: one published Delta table per subset -----------------------

# NULLIF the numeric sentinel (-999) and text sentinels ('-', '') before casting.
_FREEZE_THAW_SQL = '''
SELECT
    lakecode,
    lakename,
    lakeorriver,
    season,
    TRY_CAST(NULLIF(iceon_year,  '-999') AS INTEGER) AS iceon_year,
    TRY_CAST(NULLIF(iceon_month, '-999') AS INTEGER) AS iceon_month,
    TRY_CAST(NULLIF(iceon_day,   '-999') AS INTEGER) AS iceon_day,
    TRY_CAST(NULLIF(iceoff_year,  '-999') AS INTEGER) AS iceoff_year,
    TRY_CAST(NULLIF(iceoff_month, '-999') AS INTEGER) AS iceoff_month,
    TRY_CAST(NULLIF(iceoff_day,   '-999') AS INTEGER) AS iceoff_day,
    TRY_CAST(NULLIF(duration, '-999') AS INTEGER) AS duration_days,
    TRY_CAST(latitude  AS DOUBLE) AS latitude,
    TRY_CAST(longitude AS DOUBLE) AS longitude,
    country,
    froze,
    NULLIF(comments, '') AS comments
FROM "lake-river-ice-phenology-freeze-thaw"
WHERE lakecode IS NOT NULL AND season IS NOT NULL
'''

_PHYSICAL_SQL = '''
SELECT
    lakecode,
    lakename,
    lakeorriver,
    continent,
    country,
    NULLIF(state, '-') AS state,
    latitude   AS latitude_dms,
    longitude  AS longitude_dms,
    TRY_CAST(lat_decimal AS DOUBLE) AS latitude,
    TRY_CAST(lon_decimal AS DOUBLE) AS longitude,
    TRY_CAST(NULLIF(NULLIF(elevation,    '-999'), '-') AS DOUBLE) AS elevation_m,
    TRY_CAST(NULLIF(NULLIF(mean_depth,   '-999'), '-') AS DOUBLE) AS mean_depth_m,
    TRY_CAST(NULLIF(NULLIF(median_depth, '-999'), '-') AS DOUBLE) AS median_depth_m,
    TRY_CAST(NULLIF(NULLIF(max_depth,    '-999'), '-') AS DOUBLE) AS max_depth_m,
    TRY_CAST(NULLIF(NULLIF(surface_area, '-999'), '-') AS DOUBLE) AS surface_area_km2,
    TRY_CAST(NULLIF(NULLIF(shoreline,    '-999'), '-') AS DOUBLE) AS shoreline_km,
    TRY_CAST(NULLIF(NULLIF(largest_city_population, '-999'), '-') AS DOUBLE) AS largest_city_population,
    TRY_CAST(NULLIF(NULLIF(area_drained,    '-999'), '-') AS DOUBLE) AS area_drained_km2,
    TRY_CAST(NULLIF(NULLIF(conductivity_us, '-999'), '-') AS DOUBLE) AS conductivity_us,
    TRY_CAST(NULLIF(NULLIF(secchi_depth,    '-999'), '-') AS DOUBLE) AS secchi_depth_m,
    NULLIF(NULLIF(power_plant_discharge, '-999'), '-') AS power_plant_discharge,
    NULLIF(NULLIF(inlet_streams,         '-999'), '-') AS inlet_streams,
    NULLIF(NULLIF(landuse_code, '-999'), '-') AS landuse_code,
    NULLIF(contributor, '-') AS contributor,
    NULLIF(comments, '') AS comments
FROM "lake-river-ice-phenology-physical-characteristics"
WHERE lakecode IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="lake-river-ice-phenology-freeze-thaw-transform",
        deps=["lake-river-ice-phenology-freeze-thaw"],
        sql=_FREEZE_THAW_SQL,
    ),
    SqlNodeSpec(
        id="lake-river-ice-phenology-physical-characteristics-transform",
        deps=["lake-river-ice-phenology-physical-characteristics"],
        sql=_PHYSICAL_SQL,
    ),
]
