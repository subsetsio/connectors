"""Ember electricity data connector.

Source: Ember (ember-energy.org), open CC-BY-4.0 bulk long-format CSVs served as
static files from files.ember-energy.org (GCS-backed). Four published subsets,
one per (geographic-scope x temporal-resolution):

  - global-yearly  : ~215 countries/regions, yearly from 2000
  - global-monthly : ~88 geographies, monthly from 2018
  - us-yearly      : US state-level, yearly
  - us-monthly     : US state-level, monthly

Each file is one tidy/long table that bundles every metric Ember publishes
(generation, capacity, demand, power-sector emissions, carbon intensity) in the
Category/Subcategory/Variable columns.

Fetch shape: stateless full re-pull. Each CSV is a full snapshot (~8-105MB, no
incremental query support on the bulk path) re-fetched in full every run and
overwritten. Revisions/late corrections are picked up for free. No watermark,
no cursor.
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

_BASE = "https://files.ember-energy.org/public-downloads"

ENTITY_URLS = {
    "global-yearly": f"{_BASE}/yearly_full_release_long_format.csv",
    "global-monthly": f"{_BASE}/monthly_full_release_long_format.csv",
    "us-yearly": f"{_BASE}/us_yearly_full_release_long_format.csv",
    "us-monthly": f"{_BASE}/us_monthly_full_release_long_format.csv",
}


@transient_retry()
def _download_csv(url: str) -> bytes:
    # Bulk static CSVs; generous read timeout for the ~105MB US monthly file.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _column_types(is_us: bool, is_monthly: bool) -> dict:
    """Explicit per-column types — the contract that keeps parquet stable across
    refreshes. The period column is the only structural difference between
    yearly (integer Year) and monthly (ISO-date string Date); the geographic
    columns differ between the global (country-level) and US (state-level) files.
    """
    period_col = "Date" if is_monthly else "Year"
    period_type = pa.string() if is_monthly else pa.int64()

    if is_us:
        geo = {
            "Country": pa.string(),
            "Country code": pa.string(),
            "State": pa.string(),
            "State code": pa.string(),
            "State type": pa.string(),
        }
    else:
        geo = {
            "Area": pa.string(),
            "ISO 3 code": pa.string(),
            "Area type": pa.string(),
            "Continent": pa.string(),
            "Ember region": pa.string(),
            "EU": pa.float64(),
            "OECD": pa.float64(),
            "G20": pa.float64(),
            "G7": pa.float64(),
            "ASEAN": pa.float64(),
        }

    types = dict(geo)
    types[period_col] = period_type
    types.update(
        {
            "Category": pa.string(),
            "Subcategory": pa.string(),
            "Variable": pa.string(),
            "Unit": pa.string(),
            "Value": pa.float64(),
            "YoY absolute change": pa.float64(),
            "YoY % change": pa.float64(),
        }
    )
    return types


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("ember-"):]
    url = ENTITY_URLS[entity]
    is_us = entity.startswith("us-")
    is_monthly = entity.endswith("-monthly")

    content = _download_csv(url)

    table = pacsv.read_csv(
        io.BytesIO(content),
        read_options=pacsv.ReadOptions(use_threads=True),
        convert_options=pacsv.ConvertOptions(
            column_types=_column_types(is_us, is_monthly),
            strings_can_be_null=True,
        ),
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="ember-global-yearly", fn=fetch_one, kind="download"),
    NodeSpec(id="ember-global-monthly", fn=fetch_one, kind="download"),
    NodeSpec(id="ember-us-yearly", fn=fetch_one, kind="download"),
    NodeSpec(id="ember-us-monthly", fn=fetch_one, kind="download"),
]


# --- transforms: one published Delta table per subset -----------------------
# Thin parse/rename/cast pass. Geographic columns differ global vs US; the
# period column is INTEGER year (yearly) or DATE (monthly). Rows with a null
# Value are dropped — they carry no observation.

_GLOBAL_SELECT = """
        "Area"                          AS area,
        "ISO 3 code"                    AS iso3_code,
        "Area type"                     AS area_type,
        "Continent"                     AS continent,
        "Ember region"                  AS ember_region,
        CAST("EU" AS BOOLEAN)           AS eu,
        CAST("OECD" AS BOOLEAN)         AS oecd,
        CAST("G20" AS BOOLEAN)          AS g20,
        CAST("G7" AS BOOLEAN)           AS g7,
        CAST("ASEAN" AS BOOLEAN)        AS asean,
        "Category"                      AS category,
        "Subcategory"                   AS subcategory,
        "Variable"                      AS variable,
        "Unit"                          AS unit,
        CAST("Value" AS DOUBLE)         AS value,
        CAST("YoY absolute change" AS DOUBLE) AS yoy_absolute_change,
        CAST("YoY % change" AS DOUBLE)        AS yoy_percent_change
"""

_US_SELECT = """
        "Country"                       AS country,
        "Country code"                  AS country_code,
        "State"                         AS state,
        "State code"                    AS state_code,
        "State type"                    AS state_type,
        "Category"                      AS category,
        "Subcategory"                   AS subcategory,
        "Variable"                      AS variable,
        "Unit"                          AS unit,
        CAST("Value" AS DOUBLE)         AS value,
        CAST("YoY absolute change" AS DOUBLE) AS yoy_absolute_change,
        CAST("YoY % change" AS DOUBLE)        AS yoy_percent_change
"""


def _transform_sql(dep: str, geo_select: str, monthly: bool) -> str:
    period = (
        'CAST("Date" AS DATE) AS date' if monthly else 'CAST("Year" AS INTEGER) AS year'
    )
    return f"""
        SELECT
        {period},
        {geo_select.strip()}
        FROM "{dep}"
        WHERE "Value" IS NOT NULL
    """


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ember-global-yearly-transform",
        deps=["ember-global-yearly"],
        sql=_transform_sql("ember-global-yearly", _GLOBAL_SELECT, monthly=False),
        key=("area", "year", "category", "subcategory", "variable"),
        temporal="year",
    ),
    SqlNodeSpec(
        id="ember-global-monthly-transform",
        deps=["ember-global-monthly"],
        sql=_transform_sql("ember-global-monthly", _GLOBAL_SELECT, monthly=True),
        key=("area", "date", "category", "subcategory", "variable"),
        temporal="date",
    ),
    SqlNodeSpec(
        id="ember-us-yearly-transform",
        deps=["ember-us-yearly"],
        sql=_transform_sql("ember-us-yearly", _US_SELECT, monthly=False),
        key=("state", "year", "category", "subcategory", "variable"),
        temporal="year",
    ),
    SqlNodeSpec(
        id="ember-us-monthly-transform",
        deps=["ember-us-monthly"],
        sql=_transform_sql("ember-us-monthly", _US_SELECT, monthly=True),
        key=("state", "date", "category", "subcategory", "variable"),
        temporal="date",
    ),
]
