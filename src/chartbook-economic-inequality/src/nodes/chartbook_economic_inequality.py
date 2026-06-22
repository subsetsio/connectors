"""Chartbook of Economic Inequality connector.

Single-dataset academic source: one tidy/long Excel file (DataInput...xls) holds
the entire corpus — 25 countries, ~1900-2015, 5 inequality dimensions. The file
is small (~2MB, 18792 rows), static, and has no incremental query surface, so the
fetch is a stateless full re-pull: download the .xls, parse it to a long table,
overwrite the raw parquet. A MaintainSpec (later step) gates whether this runs.

The published subset filters to rows that actually carry a value (~4799 of 18792;
the source pre-materializes every (country, year, dimension, series) slot, most
empty) and types the columns.
"""
import io

import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

XLS_URL = (
    "https://chartbookofeconomicinequality.com/wp-content/uploads/"
    "DataForDownload/DataInput_ChartbookOfEconomicInequality.xls"
)

# The .xls sheet header (note the upstream typo 'meaure'); we rename to clean
# snake_case below.
_COLUMNS = ["country", "year", "dimension", "measure", "series", "description", "value"]

SCHEMA = pa.schema([
    ("country", pa.string()),
    ("year", pa.int64()),
    ("dimension", pa.string()),
    ("measure", pa.string()),
    ("series", pa.int64()),
    ("description", pa.string()),
    ("value", pa.float64()),
])


@transient_retry()  # 6 attempts, exponential backoff over transient errors / 5xx / 429
def _download_xls() -> bytes:
    resp = get(XLS_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    raw = _download_xls()
    df = pd.read_excel(io.BytesIO(raw), sheet_name=0, engine="xlrd")
    if list(df.columns) != [
        "country", "year", "dimension of inequality", "meaure of inequality",
        "series", "description", "value",
    ]:
        raise AssertionError(f"unexpected sheet header: {list(df.columns)!r}")
    df.columns = _COLUMNS

    # 'series' is a 1/2/3 series number; nullable in the source for empty slots.
    # Coerce to a pandas nullable integer so pyarrow maps it to int64 with nulls.
    df["series"] = df["series"].astype("Int64")
    df["year"] = df["year"].astype("int64")

    table = pa.Table.from_pandas(df[_COLUMNS], schema=SCHEMA, preserve_index=False)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="chartbook-economic-inequality-chartbook-inequality-values",
        fn=fetch_values,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="chartbook-economic-inequality-chartbook-inequality-values-transform",
        deps=["chartbook-economic-inequality-chartbook-inequality-values"],
        sql='''
            SELECT
                CAST(country     AS VARCHAR)  AS country,
                CAST(year        AS INTEGER)  AS year,
                CAST(dimension   AS VARCHAR)  AS dimension_of_inequality,
                CAST(measure     AS VARCHAR)  AS measure_of_inequality,
                CAST(series      AS INTEGER)  AS series,
                CAST(description AS VARCHAR)  AS description,
                CAST(value       AS DOUBLE)   AS value
            FROM "chartbook-economic-inequality-chartbook-inequality-values"
            WHERE value IS NOT NULL
        ''',
    ),
]
