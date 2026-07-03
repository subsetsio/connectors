"""World Bank connector.

Three subsets:

- countries   — country/aggregate reference table. From the v2 JSON REST API
                (https://api.worldbank.org/v2); small, stateless full re-pull.
- indicators  — ~29.5k indicator metadata records. From the v2 REST API;
                small, stateless full re-pull.
- values      — long-format observations (indicator x country x year) for the
                World Development Indicators (WDI) database, the World Bank's
                flagship series (GDP, population, life expectancy, CO2, ...).
                Sourced from the WDI **bulk archive** — one ~283MB ZIP holding
                the entire database as a wide CSV (all indicators x countries x
                years 1960-present). One download replaces ~1,500 per-indicator
                API sweeps (the per-indicator firehose over the full ~29.5k
                catalog was intractable — days per run); the wide CSV is
                unpivoted to long format in a single DuckDB pass and streamed to
                parquet.

The REST transport + parse helpers used by countries/indicators live in
src/utils.py (every v2 response is a two-element array [pagination_meta, data]).
"""
import os
import tempfile
import zipfile

import duckdb
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, raw_parquet_writer
from utils import (
    _fetch_all_pages,
    _nested,
    _to_float,
    _indicator_rows,
)

# ---------------------------------------------------------------------------
# countries
# ---------------------------------------------------------------------------
_COUNTRY_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("iso2_code", pa.string()),
    ("name", pa.string()),
    ("region_id", pa.string()),
    ("region_value", pa.string()),
    ("adminregion_id", pa.string()),
    ("adminregion_value", pa.string()),
    ("income_level_id", pa.string()),
    ("income_level_value", pa.string()),
    ("lending_type_id", pa.string()),
    ("lending_type_value", pa.string()),
    ("capital_city", pa.string()),
    ("longitude", pa.float64()),
    ("latitude", pa.float64()),
])


def fetch_countries(node_id: str) -> None:
    asset = node_id
    records = _fetch_all_pages("country", {}, per_page=400)
    rows = []
    for r in records:
        rows.append({
            "id": r.get("id"),
            "iso2_code": r.get("iso2Code"),
            "name": (r.get("name") or "").strip(),
            "region_id": _nested(r, "region", "id"),
            "region_value": _nested(r, "region", "value"),
            "adminregion_id": _nested(r, "adminregion", "id"),
            "adminregion_value": _nested(r, "adminregion", "value"),
            "income_level_id": _nested(r, "incomeLevel", "id"),
            "income_level_value": _nested(r, "incomeLevel", "value"),
            "lending_type_id": _nested(r, "lendingType", "id"),
            "lending_type_value": _nested(r, "lendingType", "value"),
            "capital_city": (r.get("capitalCity") or "").strip(),
            "longitude": _to_float(r.get("longitude")),
            "latitude": _to_float(r.get("latitude")),
        })
    table = pa.Table.from_pylist(rows, schema=_COUNTRY_SCHEMA)
    save_raw_parquet(table, asset)


# ---------------------------------------------------------------------------
# indicators
# ---------------------------------------------------------------------------
_INDICATOR_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("name", pa.string()),
    ("unit", pa.string()),
    ("source_id", pa.string()),
    ("source_name", pa.string()),
    ("source_note", pa.string()),
    ("source_organization", pa.string()),
    ("topic_ids", pa.string()),
    ("topic_names", pa.string()),
])


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    rows = _indicator_rows()
    table = pa.Table.from_pylist(rows, schema=_INDICATOR_SCHEMA)
    save_raw_parquet(table, asset)


# ---------------------------------------------------------------------------
# values (WDI bulk archive)
# ---------------------------------------------------------------------------
# The entire World Development Indicators database as one ZIP: a wide CSV
# (Country Name, Country Code, Indicator Name, Indicator Code, then one column
# per year) plus reference CSVs we don't need. Stable public download; redirects
# to databankfiles.worldbank.org. Refreshed on the WDI release cadence.
WDI_BULK_URL = "https://databank.worldbank.org/data/download/WDI_CSV.zip"
WDI_DATA_MEMBER = "WDICSV.csv"

# Batch size for streaming the unpivoted long table out to parquet — bounds peak
# memory; the transform's dep view glob-unions the row groups transparently.
_VALUES_BATCH_ROWS = 1_000_000

# Columns that identify a row in the wide CSV; everything else is a year column.
_WDI_ID_COLS = ("Country Name", "Country Code", "Indicator Name", "Indicator Code")


def fetch_values(node_id: str) -> None:
    # One bulk download of the whole WDI database, unpivoted wide->long. This is
    # a one-shot fetch (no watermark/continuation): the corpus is ~9M non-null
    # observations and unpivots in a single DuckDB pass in seconds.
    resp = get(WDI_BULK_URL, timeout=(30.0, 600.0))
    resp.raise_for_status()

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = os.path.join(tmp, "wdi.zip")
        with open(zip_path, "wb") as fh:
            fh.write(resp.content)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extract(WDI_DATA_MEMBER, tmp)
        csv_path = os.path.join(tmp, WDI_DATA_MEMBER)

        excluded = ", ".join(f'"{c}"' for c in _WDI_ID_COLS)
        # all_varchar: the wide CSV mixes an empty-string sentinel with numeric
        # values across ~66 year columns; read everything as text, then cast the
        # kept cells. UNPIVOT collapses the year columns into (year, value) rows;
        # empty/non-numeric cells drop out via the value filter.
        unpivot_sql = f"""
            SELECT
                "Indicator Code"        AS indicator_code,
                "Indicator Name"        AS indicator_name,
                "Country Code"          AS country_code,
                "Country Name"          AS country_name,
                CAST(year_str AS INTEGER)   AS year,
                CAST(value_str AS DOUBLE)   AS value
            FROM (
                UNPIVOT (
                    SELECT * FROM read_csv('{csv_path}', header=true, all_varchar=true)
                )
                ON COLUMNS(* EXCLUDE ({excluded}))
                INTO NAME year_str VALUE value_str
            )
            WHERE value_str IS NOT NULL
              AND TRY_CAST(value_str AS DOUBLE) IS NOT NULL
              AND TRY_CAST(year_str AS INTEGER) IS NOT NULL
        """

        con = duckdb.connect()
        try:
            reader = con.execute(unpivot_sql).fetch_record_batch(_VALUES_BATCH_ROWS)
            with raw_parquet_writer(node_id, reader.schema) as writer:
                for batch in reader:
                    writer.write_batch(batch)
        finally:
            con.close()


# ---------------------------------------------------------------------------
# specs
# ---------------------------------------------------------------------------
DOWNLOAD_SPECS = [
    NodeSpec(id="world-bank-countries", fn=fetch_countries, kind="download"),
    NodeSpec(id="world-bank-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="world-bank-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="world-bank-countries-transform",
        deps=["world-bank-countries"],
        sql='''
            SELECT
                id                  AS country_code,
                iso2_code,
                name,
                region_id,
                NULLIF(region_value, '')        AS region,
                NULLIF(income_level_value, '')  AS income_level,
                NULLIF(lending_type_value, '')  AS lending_type,
                NULLIF(capital_city, '')        AS capital_city,
                longitude,
                latitude
            FROM "world-bank-countries"
            WHERE id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="world-bank-indicators-transform",
        deps=["world-bank-indicators"],
        sql='''
            SELECT
                id                          AS indicator_code,
                name,
                NULLIF(unit, '')            AS unit,
                source_id,
                NULLIF(source_name, '')     AS source_name,
                NULLIF(source_note, '')     AS definition,
                NULLIF(source_organization, '') AS source_organization,
                NULLIF(topic_names, '')     AS topics
            FROM "world-bank-indicators"
            WHERE id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="world-bank-values-transform",
        deps=["world-bank-values"],
        key=("indicator_code", "country_code", "year"),
        temporal="year",
        sql='''
            SELECT
                indicator_code,
                indicator_name,
                country_code,
                country_name,
                year,
                value
            FROM "world-bank-values"
            WHERE value IS NOT NULL
              AND indicator_code IS NOT NULL
              AND country_code IS NOT NULL
              AND year IS NOT NULL
        ''',
    ),
]
