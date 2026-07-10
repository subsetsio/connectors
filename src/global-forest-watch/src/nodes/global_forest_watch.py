"""Global Forest Watch connector — download.

Source: GFW Data API (https://data-api.globalforestwatch.org) — FastAPI, fully
open (no API key) for the catalog and the ``/download/csv`` endpoint, which runs
read-only SQL over each dataset-version's table (aliased ``data``).

Shape of the source: GFW stores its statistical products as enormous
denormalised cross-tabulations — one row per administrative area x *every*
context-overlay combination (protected-area status, primary-forest flag,
plantation type, mining concession, ... 20-60 such dimension columns), with the
actual measures (hectares, tonnes CO2e, alert counts) at the end. A single
``SELECT *`` over these tables returns millions of rows and 502s past the API's
~90k-row / 6MB per-request Lambda ceiling.

Strategy: collapse each table to a **tidy statistical grain** server-side in the
download SQL — GROUP BY the core dimensions (iso / admin unit / protected-area
id, the observation period, and the canopy-density threshold or alert
confidence) and SUM the measures across the dropped context overlays. This both
produces analysis-ready raw (the model stage then publishes it near-verbatim)
and shrinks each fetch by 1-2 orders of magnitude. Results that still exceed the
row cap are paged with ``ORDER BY <grain> LIMIT/OFFSET`` (subqueries are
rejected by the endpoint, so paging is applied to the flat GROUP BY directly;
the grain columns form a total order, so OFFSET paging neither skips nor dups).

The small FAO national forest-statistics tables (<1k rows) are pulled verbatim.
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv
from subsets_utils import NodeSpec, get, save_raw_parquet, transient_retry

BASE = "https://data-api.globalforestwatch.org"

# Page size for results over the API's ~90k-row / 6MB per-request ceiling. Kept
# well under it for margin on wide rows.
PAGE = 45000

# Postgres backs the endpoint: mixed-case / spaced column names MUST be
# double-quoted or they are silently lower-cased and "not found". Each entry is
# (select_body, order_by): the fetcher appends `ORDER BY <order_by> LIMIT n
# OFFSET m`. Float measures are CAST to double precision so the CSV always
# carries a decimal point and pyarrow infers a stable type across pages.
QUERIES: dict[str, tuple[str, str]] = {
    # ---- FAO national forest statistics (verbatim; small, clean) ----------
    "fao_forest_extent": (
        'SELECT iso, country, desk_study, year, '
        '"primary (ha)" AS primary_ha, '
        '"naturally regenerating forest (ha)" AS naturally_regenerating_forest_ha, '
        '"planted forest (ha)" AS planted_forest_ha, '
        '"forest (ha)" AS forest_ha, '
        '"non-forest (ha)" AS non_forest_ha, '
        '"total land area (ha)" AS total_land_area_ha '
        'FROM data',
        "iso, year, desk_study",
    ),
    "fao_forest_change": (
        # `year` here is a reporting *period* range ("2000-2010"), not a point
        # year — alias it accordingly.
        'SELECT iso, country, desk_study, year AS period, '
        '"reforestation (ha per year)" AS reforestation_ha_per_year, '
        '"forest expansion (ha per year)" AS forest_expansion_ha_per_year, '
        '"deforestation (ha per year)" AS deforestation_ha_per_year '
        'FROM data',
        "iso, period, desk_study",
    ),
    "fao_forestry_employment": (
        'SELECT iso, country, desk_study, year, '
        '"silviculture and other (FTE)" AS silviculture_and_other_fte, '
        '"logging (FTE)" AS logging_fte, '
        '"gathering (FTE)" AS gathering_fte, '
        '"support (FTE)" AS support_fte, '
        '"all (FTE)" AS all_fte, '
        '"female (FTE)" AS female_fte '
        'FROM data',
        "iso, year, desk_study",
    ),
    "fao_management_objectives": (
        'SELECT iso, country, desk_study, year, '
        '"production (ha)" AS production_ha, '
        '"protection of soil and water (ha)" AS protection_soil_water_ha, '
        '"conservation of biodiversity (ha)" AS conservation_biodiversity_ha, '
        '"social services (ha)" AS social_services_ha, '
        '"multiple use (ha)" AS multiple_use_ha, '
        '"other (ha)" AS other_ha, '
        '"none or unknown (ha)" AS none_or_unknown_ha '
        'FROM data',
        "iso, year, desk_study",
    ),
    # ---- GADM tree-cover-loss / carbon summary by country x threshold -----
    "gadm__tcl__iso_summary": (
        'SELECT iso, '
        '"umd_tree_cover_density_2000__threshold" AS canopy_density_threshold, '
        'CAST(SUM("area__ha") AS double precision) AS area_ha, '
        'CAST(SUM("umd_tree_cover_extent_2000__ha") AS double precision) AS tree_cover_extent_2000_ha, '
        'CAST(SUM("umd_tree_cover_extent_2010__ha") AS double precision) AS tree_cover_extent_2010_ha, '
        'CAST(SUM("umd_tree_cover_gain__ha") AS double precision) AS tree_cover_gain_ha, '
        'CAST(SUM("umd_tree_cover_loss__ha") AS double precision) AS tree_cover_loss_ha, '
        'CAST(SUM("umd_tree_cover_loss_from_fires__ha") AS double precision) AS tree_cover_loss_from_fires_ha, '
        'CAST(SUM("gfw_aboveground_carbon_stocks_2000__Mg_C") AS double precision) AS aboveground_carbon_stocks_2000_mg_c, '
        'CAST(SUM("gfw_belowground_carbon_stocks_2000__Mg_C") AS double precision) AS belowground_carbon_stocks_2000_mg_c, '
        'CAST(SUM("gfw_soil_carbon_stocks_2000__Mg_C") AS double precision) AS soil_carbon_stocks_2000_mg_c, '
        'CAST(SUM("whrc_aboveground_biomass_stock_2000__Mg") AS double precision) AS aboveground_biomass_stock_2000_mg, '
        'CAST(SUM("gfw_full_extent_gross_emissions__Mg_CO2e") AS double precision) AS gross_emissions_mg_co2e, '
        'CAST(SUM("gfw_full_extent_gross_removals__Mg_CO2") AS double precision) AS gross_removals_mg_co2, '
        'CAST(SUM("gfw_full_extent_net_flux__Mg_CO2e") AS double precision) AS net_flux_mg_co2e '
        'FROM data '
        'GROUP BY iso, "umd_tree_cover_density_2000__threshold"',
        "iso, canopy_density_threshold",
    ),
    # ---- GADM GLAD deforestation-alert AREA summaries (cumulative) ---------
    "gadm__glad__iso_summary": (
        'SELECT iso, '
        'CAST(SUM("alert_area__ha") AS double precision) AS alert_area_ha '
        'FROM data GROUP BY iso',
        "iso",
    ),
    "gadm__glad__adm1_summary": (
        'SELECT iso, adm1, '
        'CAST(SUM("alert_area__ha") AS double precision) AS alert_area_ha '
        'FROM data GROUP BY iso, adm1',
        "iso, adm1",
    ),
    "gadm__glad__adm2_summary": (
        'SELECT iso, adm1, adm2, '
        'CAST(SUM("alert_area__ha") AS double precision) AS alert_area_ha '
        'FROM data GROUP BY iso, adm1, adm2',
        "iso, adm1, adm2",
    ),
    # ---- GADM weekly alert time series by country -------------------------
    "gadm__glad__iso_weekly_alerts": (
        'SELECT iso, "alert__year" AS alert_year, "alert__week" AS alert_week, '
        'CAST("is__confirmed_alert" AS text) AS is_confirmed_alert, '
        'CAST(SUM("alert__count") AS bigint) AS alert_count, '
        'CAST(SUM("alert_area__ha") AS double precision) AS alert_area_ha, '
        'CAST(SUM("whrc_aboveground_co2_emissions__Mg") AS double precision) AS aboveground_co2_emissions_mg '
        'FROM data GROUP BY iso, "alert__year", "alert__week", "is__confirmed_alert"',
        "iso, alert_year, alert_week, is_confirmed_alert",
    ),
    "gadm__burned_areas__iso_weekly_alerts": (
        'SELECT iso, "alert__year" AS alert_year, "alert__week" AS alert_week, '
        'CAST(SUM("burned_area__ha") AS double precision) AS burned_area_ha '
        'FROM data GROUP BY iso, "alert__year", "alert__week"',
        "iso, alert_year, alert_week",
    ),
    "gadm__viirs__iso_weekly_alerts": (
        'SELECT iso, "alert__year" AS alert_year, "alert__week" AS alert_week, '
        '"confidence__cat" AS confidence, '
        'CAST(SUM("alert__count") AS bigint) AS alert_count '
        'FROM data GROUP BY iso, "alert__year", "alert__week", "confidence__cat"',
        "iso, alert_year, alert_week, confidence",
    ),
    # ---- WDPA protected-area alert products (keyed by protected-area id) ---
    "wdpa_protected_areas__glad__summary": (
        'SELECT "wdpa_protected_area__id" AS wdpa_id, '
        '"wdpa_protected_area__name" AS wdpa_name, '
        '"wdpa_protected_area__iucn_cat" AS iucn_cat, '
        '"wdpa_protected_area__iso" AS iso, '
        '"wdpa_protected_area__status" AS status, '
        'CAST(SUM("alert_area__ha") AS double precision) AS alert_area_ha '
        'FROM data GROUP BY "wdpa_protected_area__id", "wdpa_protected_area__name", '
        '"wdpa_protected_area__iucn_cat", "wdpa_protected_area__iso", "wdpa_protected_area__status"',
        "wdpa_id",
    ),
    "wdpa_protected_areas__glad__daily_alerts": (
        'SELECT "wdpa_protected_area__id" AS wdpa_id, '
        '"wdpa_protected_area__name" AS wdpa_name, '
        '"wdpa_protected_area__iucn_cat" AS iucn_cat, '
        '"wdpa_protected_area__iso" AS iso, '
        '"wdpa_protected_area__status" AS status, '
        '"umd_glad_landsat_alerts__date" AS alert_date, '
        '"umd_glad_landsat_alerts__confidence" AS confidence, '
        'CAST(SUM("alert__count") AS bigint) AS alert_count, '
        'CAST(SUM("alert_area__ha") AS double precision) AS alert_area_ha, '
        'CAST(SUM("whrc_aboveground_co2_emissions__Mg") AS double precision) AS aboveground_co2_emissions_mg '
        'FROM data GROUP BY "wdpa_protected_area__id", "wdpa_protected_area__name", '
        '"wdpa_protected_area__iucn_cat", "wdpa_protected_area__iso", "wdpa_protected_area__status", '
        '"umd_glad_landsat_alerts__date", "umd_glad_landsat_alerts__confidence"',
        "wdpa_id, alert_date, confidence",
    ),
    "wdpa_protected_areas__glad__weekly_alerts": (
        'SELECT "wdpa_protected_area__id" AS wdpa_id, '
        '"wdpa_protected_area__name" AS wdpa_name, '
        '"wdpa_protected_area__iucn_cat" AS iucn_cat, '
        '"wdpa_protected_area__iso" AS iso, '
        '"wdpa_protected_area__status" AS status, '
        '"alert__year" AS alert_year, "alert__week" AS alert_week, '
        'CAST("is__confirmed_alert" AS text) AS is_confirmed_alert, '
        'CAST(SUM("alert__count") AS bigint) AS alert_count, '
        'CAST(SUM("alert_area__ha") AS double precision) AS alert_area_ha, '
        'CAST(SUM("whrc_aboveground_co2_emissions__Mg") AS double precision) AS aboveground_co2_emissions_mg '
        'FROM data GROUP BY "wdpa_protected_area__id", "wdpa_protected_area__name", '
        '"wdpa_protected_area__iucn_cat", "wdpa_protected_area__iso", "wdpa_protected_area__status", '
        '"alert__year", "alert__week", "is__confirmed_alert"',
        "wdpa_id, alert_year, alert_week, is_confirmed_alert",
    ),
    "wdpa_protected_areas__viirs__weekly_alerts": (
        'SELECT "wdpa_protected_area__id" AS wdpa_id, '
        '"wdpa_protected_area__name" AS wdpa_name, '
        '"wdpa_protected_area__iucn_cat" AS iucn_cat, '
        '"wdpa_protected_area__iso" AS iso, '
        '"wdpa_protected_area__status" AS status, '
        '"alert__year" AS alert_year, "alert__week" AS alert_week, '
        '"confidence__cat" AS confidence, '
        'CAST(SUM("alert__count") AS bigint) AS alert_count '
        'FROM data GROUP BY "wdpa_protected_area__id", "wdpa_protected_area__name", '
        '"wdpa_protected_area__iucn_cat", "wdpa_protected_area__iso", "wdpa_protected_area__status", '
        '"alert__year", "alert__week", "confidence__cat"',
        "wdpa_id, alert_year, alert_week, confidence",
    ),
}


def _asset_id(entity_id: str) -> str:
    return f"global-forest-watch-{entity_id.lower().replace('_', '-')}"


_ASSET_TO_ENTITY = {_asset_id(e): e for e in QUERIES}


@transient_retry()
def _get_json(url: str) -> dict:
    r = get(url, timeout=(10.0, 60.0))
    r.raise_for_status()
    return r.json()


@transient_retry()
def _get_csv(url: str, sql: str) -> bytes:
    # API Gateway 504s on slow queries and 429s under load — both 5xx/429, so
    # transient_retry backs off and retries; a 4xx query error reraises loudly.
    r = get(url, params={"sql": sql}, timeout=(10.0, 300.0))
    r.raise_for_status()
    return r.content


def _resolve_version(entity_id: str) -> str:
    """Newest immutable dataset version. GFW's 'latest' pointer is unreliable
    (some datasets report 'no latest version'), so resolve the max dated version
    directly — versions within a dataset share one scheme and sort correctly."""
    versions = _get_json(f"{BASE}/dataset/{entity_id}")["data"]["versions"]
    if not versions:
        raise RuntimeError(f"{entity_id}: no versions published")
    return max(versions)


def fetch_one(asset_id: str) -> None:
    """Fetch one tidy statistical subset as parquet, paging the aggregated query
    under the API's per-request ceiling. The runtime passes the spec id (also the
    raw asset name); the entity is recovered from it."""
    entity_id = _ASSET_TO_ENTITY[asset_id]
    version = _resolve_version(entity_id)
    body, order_by = QUERIES[entity_id]
    url = f"{BASE}/dataset/{entity_id}/{version}/download/csv"

    parts: list[pa.Table] = []
    offset = 0
    while True:
        sql = f"{body} ORDER BY {order_by} LIMIT {PAGE} OFFSET {offset}"
        table = pacsv.read_csv(io.BytesIO(_get_csv(url, sql)))
        n = table.num_rows
        if n:
            parts.append(table)
        if n < PAGE:
            break
        offset += PAGE
        if offset > 100_000_000:  # runaway guard — no GFW table is this large
            raise RuntimeError(f"{asset_id}: paging exceeded 100M rows for {entity_id} {version}")

    total = sum(p.num_rows for p in parts)
    if total == 0:
        raise RuntimeError(f"{asset_id}: /download/csv returned 0 rows for {entity_id} {version}")
    table = parts[0] if len(parts) == 1 else pa.concat_tables(parts, promote_options="permissive")
    save_raw_parquet(table, asset_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=_asset_id(e), fn=fetch_one, kind="download") for e in QUERIES
]
