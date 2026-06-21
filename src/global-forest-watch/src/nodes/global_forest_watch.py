"""Global Forest Watch connector.

Source: GFW Data API (https://data-api.globalforestwatch.org) — FastAPI, fully
open (no API key) for the catalog and the /download/csv endpoint, which runs
read-only SQL over each dataset-version's table (aliased ``data``).

Strategy: every published subset is a country (iso) level statistical table.
The small national tables (FAO forest stats, the global power-plant database,
the universal mill list) are pulled verbatim. The flagship GFW products
(tree-cover-loss / emissions, carbon flux, integrated deforestation alerts) are
stored upstream as enormous denormalised cross-tabulations (tens of millions of
rows, one per admin area x every overlay dimension). Those are collapsed to a
tidy country-level time series **server-side** in the download SQL via GROUP BY,
so each fetch returns well under the API's ~90k-row / 6MB per-request ceiling in
a single request — no pagination, no API key.
"""

import io

import httpx
import pyarrow.csv as pacsv
import subsets_utils as su
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

BASE = "https://data-api.globalforestwatch.org"

# The rank-accepted entity union (9 country-level statistical datasets).
ENTITY_IDS = [
    "fao_forest_extent",
    "fao_forest_change",
    "fao_forestry_employment",
    "gadm__tcl__iso_change",
    "gadm__tcl__iso_summary",
    "carbonflux_iso_summary",
    "gadm__integrated_alerts__iso_daily_alerts",
    "wri_global_power_plant_database",
    "gfw_universal_mill_list",
]

# One SQL query per entity, executed by the /download/csv endpoint over the
# table aliased ``data``. The backend is Postgres-style: mixed-case column names
# MUST be double-quoted or they are silently lower-cased and "not found". Each
# query is verified to return 200 with the shape below in one request.
QUERIES = {
    # National forest statistics (verbatim, clean country x year tables).
    "fao_forest_extent": (
        'SELECT iso, country, desk_study, year, '
        '"primary (ha)" AS primary_ha, '
        '"naturally regenerating forest (ha)" AS naturally_regenerating_forest_ha, '
        '"planted forest (ha)" AS planted_forest_ha, '
        '"forest (ha)" AS forest_ha, '
        '"non-forest (ha)" AS non_forest_ha, '
        '"total land area (ha)" AS total_land_area_ha '
        'FROM data'
    ),
    "fao_forest_change": (
        # `year` here is a reporting *period* range ("2000-2010"), not a point
        # year — name it accordingly so it doesn't collide types with the
        # point-year `year` in the other tables.
        'SELECT iso, country, desk_study, year AS period, '
        '"reforestation (ha per year)" AS reforestation_ha_per_year, '
        '"forest expansion (ha per year)" AS forest_expansion_ha_per_year, '
        '"deforestation (ha per year)" AS deforestation_ha_per_year '
        'FROM data'
    ),
    "fao_forestry_employment": (
        'SELECT iso, country, desk_study, year, '
        '"silviculture and other (FTE)" AS silviculture_and_other_fte, '
        '"logging (FTE)" AS logging_fte, '
        '"gathering (FTE)" AS gathering_fte, '
        '"support (FTE)" AS support_fte, '
        '"all (FTE)" AS all_fte, '
        '"female (FTE)" AS female_fte '
        'FROM data'
    ),
    # Tree cover loss & gross emissions by country / year / canopy-density
    # threshold (10M-row cross-tab collapsed to ~40k tidy rows).
    "gadm__tcl__iso_change": (
        'SELECT iso, '
        '"umd_tree_cover_loss__year" AS year, '
        '"umd_tree_cover_density_2000__threshold" AS canopy_density_threshold, '
        'SUM("umd_tree_cover_loss__ha") AS tree_cover_loss_ha, '
        'SUM("umd_tree_cover_loss_from_fires__ha") AS tree_cover_loss_from_fires_ha, '
        'SUM("whrc_aboveground_biomass_loss__Mg") AS aboveground_biomass_loss_mg, '
        'SUM("whrc_aboveground_co2_emissions__Mg") AS aboveground_co2_emissions_mg, '
        'SUM("gfw_full_extent_gross_emissions__Mg_CO2e") AS gross_emissions_co2e_mg '
        'FROM data '
        'GROUP BY iso, "umd_tree_cover_loss__year", "umd_tree_cover_density_2000__threshold"'
    ),
    # Tree cover extent / gain / carbon stocks by country / threshold (no year:
    # a cumulative snapshot).
    "gadm__tcl__iso_summary": (
        'SELECT iso, '
        '"umd_tree_cover_density_2000__threshold" AS canopy_density_threshold, '
        'SUM("umd_tree_cover_extent_2000__ha") AS tree_cover_extent_2000_ha, '
        'SUM("umd_tree_cover_extent_2010__ha") AS tree_cover_extent_2010_ha, '
        'SUM("umd_tree_cover_gain__ha") AS tree_cover_gain_ha, '
        'SUM("umd_tree_cover_loss__ha") AS tree_cover_loss_ha, '
        'SUM("area__ha") AS area_ha, '
        'SUM("gfw_aboveground_carbon_stocks_2000__Mg_C") AS aboveground_carbon_stocks_2000_mg_c, '
        'SUM("whrc_aboveground_biomass_stock_2000__Mg") AS aboveground_biomass_stock_2000_mg '
        'FROM data '
        'GROUP BY iso, "umd_tree_cover_density_2000__threshold"'
    ),
    # Forest carbon flux model summary by country / threshold.
    "carbonflux_iso_summary": (
        'SELECT iso, '
        '"umd_tree_cover_density_2000__threshold" AS canopy_density_threshold, '
        'SUM("gfw_flux_model_extent__ha") AS flux_model_extent_ha, '
        'SUM("gfw_full_extent_gross_emissions_biomass_soil__Mg_CO2e") AS gross_emissions_co2e_mg, '
        'SUM("gfw_full_extent_gross_removals__Mg_CO2") AS gross_removals_co2_mg '
        'FROM data '
        'GROUP BY iso, "umd_tree_cover_density_2000__threshold"'
    ),
    # Integrated deforestation alerts (GLAD-L + GLAD-S2 + RADD) by country /
    # month / confidence (3.97M daily rows collapsed to ~8k monthly rows).
    "gadm__integrated_alerts__iso_daily_alerts": (
        'SELECT iso, '
        'CAST(date_part(\'year\', "gfw_integrated_alerts__date") AS INTEGER) AS year, '
        'CAST(date_part(\'month\', "gfw_integrated_alerts__date") AS INTEGER) AS month, '
        '"gfw_integrated_alerts__confidence" AS confidence, '
        'SUM("alert__count") AS alert_count, '
        'SUM("alert_area__ha") AS alert_area_ha '
        'FROM data '
        'WHERE "gfw_integrated_alerts__date" IS NOT NULL '
        'GROUP BY iso, year, month, confidence'
    ),
    # Global power-plant database (verbatim; lat/long are plain numeric columns).
    "wri_global_power_plant_database": "SELECT * FROM data",
    # Universal mill list (verbatim minus the geometry blobs and the constant /
    # empty columns: gfw_area__ha is 0 for every row, created_on/updated_on are
    # load timestamps, date_rspo_ is a single constant date).
    "gfw_universal_mill_list": (
        'SELECT gfw_fid, uml_id, parent_com, mill_name, rspo_statu, rspo_type, '
        'latitude, longitude, country, province, district, '
        'confidence, alternativ, gfw_geostore_id '
        'FROM data'
    ),
}


def _asset_id(entity_id: str) -> str:
    return f"global-forest-watch-{entity_id.lower().replace('_', '-')}"


_ASSET_TO_ENTITY = {_asset_id(e): e for e in ENTITY_IDS}


class _TransientHTTP(Exception):
    """A retryable upstream condition (5xx / 429 / gateway timeout)."""


@retry(
    retry=retry_if_exception_type((_TransientHTTP, httpx.TransportError)),
    wait=wait_exponential(multiplier=2, min=2, max=60),
    stop=stop_after_attempt(6),
    reraise=True,
)
def _get(url: str, *, timeout: float, params: dict | None = None) -> httpx.Response:
    r = su.get(url, params=params, timeout=timeout)
    # API Gateway emits 504 on slow queries and 429 under load; both are worth a
    # backed-off retry. Everything else (incl. 4xx query errors) is terminal.
    if r.status_code in (429,) or r.status_code >= 500:
        raise _TransientHTTP(f"{r.status_code} from {url}: {r.text[:200]}")
    r.raise_for_status()
    return r


def _resolve_version(entity_id: str) -> str:
    """Newest immutable dataset version. GFW's 'latest' pointer is unreliable
    (some datasets report 'no latest version'), so resolve the max dated version
    directly — they sort lexicographically within a dataset's scheme."""
    r = _get(f"{BASE}/dataset/{entity_id}", timeout=60)
    versions = r.json()["data"]["versions"]
    if not versions:
        raise RuntimeError(f"{entity_id}: no versions published")
    return max(versions)


def fetch_one(asset_id: str) -> None:
    """Fetch one country-level subset as parquet. The runtime passes the spec id
    (also the raw asset name); the entity is recovered from it."""
    entity_id = _ASSET_TO_ENTITY[asset_id]
    version = _resolve_version(entity_id)
    sql = QUERIES[entity_id]
    r = _get(
        f"{BASE}/dataset/{entity_id}/{version}/download/csv",
        params={"sql": sql},
        timeout=300,
    )
    table = pacsv.read_csv(io.BytesIO(r.content))
    if table.num_rows == 0:
        raise RuntimeError(
            f"{asset_id}: /download/csv returned 0 rows for {entity_id} {version}"
        )
    save_raw_parquet(table, asset_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=_asset_id(e), fn=fetch_one, kind="download") for e in ENTITY_IDS
]

# Each subset is already tidy at fetch time, so the transform is a straight
# publish of the raw table (full snapshot -> overwrite).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_asset_id(e)}-transform",
        deps=(_asset_id(e),),
        sql=f'SELECT * FROM "{_asset_id(e)}"',
    )
    for e in ENTITY_IDS
]
