"""Federal Reserve Bank of Minneapolis connector.

Two machine-readable surfaces (see research):

* idda_bulk_csv  — Income Distributions and Dynamics in America (IDDA), a joint
  Minneapolis Fed / U.S. Census Bureau dataset. Five statistical modules, each
  published as one Delta table. Per module we fetch the `<module>_all_data.csv`
  superset (US + all states, both income types) and the `na_<module>_all_data.csv`
  native-area file, and union them with DuckDB `union_by_name` (the native files
  omit the top-tail percentile columns, so geography is a value, not a schema
  split). The two largest modules are ~200 MB / ~2M rows, so we stream DuckDB
  record batches straight into a Parquet writer to bound memory.

* cpi_scrape     — two static-HTML historical CPI tables (1800- and 1913-),
  parsed with pandas.read_html and unioned into one table with a `series`
  discriminator column.

Full re-pull every run (stateless): neither surface supports incremental
queries and the corpus is small enough to refetch in minutes. The maintain step
(authored later) decides whether a node runs on a given refresh.
"""

import io
import os
import tempfile

import duckdb
import pandas as pd
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

SLUG = "federal-reserve-bank-of-minneapolis"
PREFIX = f"{SLUG}-"

IDDA_BASE = "https://www.minneapolisfed.org/-/media/assets/institute/census/data-center"

# IDDA statistical modules. Slug (entity id, dashes) -> CSV file stem (underscores).
IDDA_MODULES = {
    "pctl-of-inc": "pctl_of_inc",
    "inc-share": "inc_share",
    "prop-share": "prop_share",
    "inc-change-distributions": "inc_change_distributions",
    "transition-matrix": "transition_matrix",
}

CPI_PAGES = [
    (
        "cpi_1800",
        "https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1800-",
    ),
    (
        "cpi_1913",
        "https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-",
    ),
]


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #
@transient_retry()
def _download_bytes(url: str) -> bytes:
    # 300s read budget — the largest IDDA module CSV is ~210 MB.
    resp = get(url, timeout=(15.0, 300.0))
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _download_text(url: str) -> str:
    resp = get(url, timeout=(15.0, 120.0))
    resp.raise_for_status()
    return resp.text


# --------------------------------------------------------------------------- #
# IDDA modules
# --------------------------------------------------------------------------- #
def fetch_idda_module(node_id: str) -> None:
    """Fetch one IDDA module: the all_data superset + the native-area file,
    unioned by column name and streamed to a single Parquet raw asset."""
    asset = node_id
    module = node_id[len(PREFIX):].replace("-", "_")
    variants = [f"{module}_all_data", f"na_{module}_all_data"]

    with tempfile.TemporaryDirectory() as tmp:
        local_paths = []
        for variant in variants:
            content = _download_bytes(f"{IDDA_BASE}/{variant}.csv")
            # Scratch copy on local disk so DuckDB can stream-parse it; this is
            # an intermediate temp file, NOT a raw asset (those go through
            # save_raw_*/raw_parquet_writer below).
            path = os.path.join(tmp, f"{variant}.csv")
            with open(path, "wb") as fh:
                fh.write(content)
            local_paths.append(path)
            del content

        con = duckdb.connect()
        try:
            files = ", ".join("'" + p + "'" for p in local_paths)
            query = (
                f"SELECT * FROM read_csv([{files}], "
                "union_by_name=true, sample_size=-1)"
            )
            reader = con.execute(query).fetch_record_batch(200_000)
            with raw_parquet_writer(asset, reader.schema) as writer:
                for batch in reader:
                    writer.write_batch(batch)
        finally:
            con.close()


# --------------------------------------------------------------------------- #
# Historical CPI scrape
# --------------------------------------------------------------------------- #
def fetch_cpi(node_id: str) -> None:
    """Scrape the two historical CPI tables and union them with a `series`
    discriminator. Columns by position: year, annual average index, percent
    change. Values are kept as the source renders them (year may carry a '*'
    preliminary marker; percent change carries a '%') and typed in the SQL
    transform."""
    asset = node_id
    rows = []
    for series, url in CPI_PAGES:
        html = _download_text(url)
        tables = pd.read_html(io.StringIO(html))
        if not tables:
            raise AssertionError(f"{series}: no HTML table found at {url}")
        table = max(tables, key=lambda t: t.shape[0])
        if table.shape[1] < 3:
            raise AssertionError(
                f"{series}: expected >=3 columns, got {table.shape[1]}"
            )
        for _, rec in table.iterrows():
            year = rec.iloc[0]
            index = rec.iloc[1]
            pct = rec.iloc[2]
            if pd.isna(year):
                continue
            rows.append(
                {
                    "series": series,
                    "year": str(year).strip(),
                    "annual_average_index": None if pd.isna(index) else float(index),
                    "annual_percent_change": None if pd.isna(pct) else str(pct).strip(),
                }
            )

    schema = pa.schema(
        [
            ("series", pa.string()),
            ("year", pa.string()),
            ("annual_average_index", pa.float64()),
            ("annual_percent_change", pa.string()),
        ]
    )
    save_raw_parquet(pa.Table.from_pylist(rows, schema=schema), asset)


# --------------------------------------------------------------------------- #
# DOWNLOAD_SPECS — one per entity-union entry
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{slug}", fn=fetch_idda_module, kind="download")
    for slug in IDDA_MODULES
] + [
    NodeSpec(id=f"{PREFIX}cpi-historical", fn=fetch_cpi, kind="download"),
]


# --------------------------------------------------------------------------- #
# TRANSFORM_SPECS — one published Delta table per subset
# --------------------------------------------------------------------------- #
# IDDA modules keyed by calendar year (single observation year).
_YEAR_MODULES = ["pctl-of-inc", "inc-share", "prop-share"]
# IDDA modules keyed by a (base year, end year) pair instead of a single year.
_PAIR_MODULES = ["inc-change-distributions", "transition-matrix"]

_idda_year_transforms = [
    SqlNodeSpec(
        id=f"{PREFIX}{slug}-transform",
        deps=[f"{PREFIX}{slug}"],
        sql=f'''
            SELECT CAST(year AS INTEGER) AS year, * EXCLUDE (year)
            FROM "{PREFIX}{slug}"
            WHERE year IS NOT NULL
        ''',
    )
    for slug in _YEAR_MODULES
]

_idda_pair_transforms = [
    SqlNodeSpec(
        id=f"{PREFIX}{slug}-transform",
        deps=[f"{PREFIX}{slug}"],
        sql=f'''
            SELECT
                CAST(y0 AS INTEGER) AS y0,
                CAST(y1 AS INTEGER) AS y1,
                * EXCLUDE (y0, y1)
            FROM "{PREFIX}{slug}"
            WHERE y0 IS NOT NULL AND y1 IS NOT NULL
        ''',
    )
    for slug in _PAIR_MODULES
]

_cpi_transform = SqlNodeSpec(
    id=f"{PREFIX}cpi-historical-transform",
    deps=[f"{PREFIX}cpi-historical"],
    sql=f'''
        SELECT
            series,
            CAST(regexp_replace(year, '[^0-9]', '', 'g') AS INTEGER) AS year,
            (year LIKE '%*%') AS preliminary,
            CAST(annual_average_index AS DOUBLE) AS annual_average_index,
            TRY_CAST(replace(annual_percent_change, '%', '') AS DOUBLE)
                AS annual_percent_change
        FROM "{PREFIX}cpi-historical"
        WHERE year IS NOT NULL
          AND regexp_replace(year, '[^0-9]', '', 'g') <> ''
          AND annual_average_index IS NOT NULL
    ''',
)

TRANSFORM_SPECS = _idda_year_transforms + _idda_pair_transforms + [_cpi_transform]
