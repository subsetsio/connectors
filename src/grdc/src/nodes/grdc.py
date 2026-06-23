"""GRDC — Global Runoff Data Centre station catalogue.

Single bulk JSON file (the complete ~11,879-station catalogue) published as one
Delta table. The actual discharge time series are NOT freely available (gated
behind a manual request/email-approval workflow), so this station catalogue —
identity, location, catchment area and discharge summary statistics per gauging
station — is the publishable statistical product.

Stateless full re-pull: the whole corpus is one ~9MB JSON GET, so we re-fetch
the entire file every run and overwrite. Raw is saved as NDJSON because column
types drift across records (e.g. `area` is int or float, period fields are
float-or-null, `*_day`/`*_month` are int-or-empty-string); the transform
re-types and cleans sentinel values (-999 = missing).
"""

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

CATALOGUE_URL = "https://portal.grdc.bafg.de/grdc/grdc_sample_records.json"


@transient_retry()
def _fetch_catalogue() -> list:
    # subsets_utils.get sets a browser-like User-Agent (verified to return 200;
    # the bafg portal 400s the default curl UA). Full corpus in one response.
    resp = get(CATALOGUE_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise TypeError(f"expected a JSON array, got {type(data).__name__}")
    return data


def fetch_station_catalogue(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    rows = _fetch_catalogue()
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="grdc-station-catalogue", fn=fetch_station_catalogue, kind="download"),
]


_STATION_SQL = '''
    SELECT
        CAST(grdc_no AS BIGINT)                       AS grdc_no,
        TRY_CAST(wmo_reg AS INTEGER)                  AS wmo_region,
        TRY_CAST(sub_reg AS INTEGER)                  AS sub_region,
        river,
        station,
        country,
        nat_id,
        CAST(ds_stat_no AS VARCHAR)                   AS downstream_station_no,
        CAST(lat AS DOUBLE)                           AS latitude,
        CAST("long" AS DOUBLE)                        AS longitude,
        NULLIF(TRY_CAST(area AS DOUBLE), -999)        AS catchment_area_km2,
        NULLIF(TRY_CAST(altitude AS DOUBLE), -999)    AS altitude_m,
        TRY_CAST(d_start AS INTEGER)                  AS daily_start_year,
        TRY_CAST(d_end AS INTEGER)                    AS daily_end_year,
        TRY_CAST(d_yrs AS DOUBLE)                     AS daily_years,
        TRY_CAST(d_miss AS DOUBLE)                    AS daily_missing_pct,
        TRY_CAST(m_start AS INTEGER)                  AS monthly_start_year,
        TRY_CAST(m_end AS INTEGER)                    AS monthly_end_year,
        TRY_CAST(m_yrs AS DOUBLE)                     AS monthly_years,
        TRY_CAST(m_miss AS DOUBLE)                    AS monthly_missing_pct,
        TRY_CAST(t_start AS INTEGER)                  AS record_start_year,
        TRY_CAST(t_end AS INTEGER)                    AS record_end_year,
        TRY_CAST(t_yrs AS DOUBLE)                     AS record_years,
        TRY_CAST(lta_discharge AS DOUBLE)             AS lta_discharge_m3s,
        TRY_CAST(r_volume_yr AS DOUBLE)               AS runoff_volume_km3_yr,
        TRY_CAST(r_height_yr AS DOUBLE)               AS runoff_height_mm_yr,
        NULLIF(TRY_CAST(provider_id AS INTEGER), -999) AS provider_id,
        TRY_CAST(l_im_yr AS INTEGER)                  AS last_import_year,
        timeseries_type,
        region_name,
        subregion_name,
        ocean,
        river_basin
    FROM "grdc-station-catalogue"
    WHERE grdc_no IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="grdc-station-catalogue-transform",
        deps=["grdc-station-catalogue"],
        sql=_STATION_SQL,
    ),
]
