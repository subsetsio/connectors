"""GCIP — Global Consumption and Income Project (Global Income Dataset).

Single static bulk CSV archived at the jackblun/Globalinc GitHub mirror (the
official gcip.info project is discontinued and its domain is now parked). One
fetch of one stable raw URL returns the entire income-decile panel: one row per
country-year, columns for income deciles 1-10, mean income, and population.
Incomes are monthly real, 2005 USD PPP.

Fetch shape: stateless full re-pull (shape 1). The corpus is ~500KB / ~4900
rows in a single immutable file — re-fetch and overwrite every run; no state,
no watermark, no incremental filter (the source exposes none — it is a static
archived artefact).
"""

import csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, save_raw_parquet

CSV_URL = "https://raw.githubusercontent.com/jackblun/Globalinc/master/GCIPrawdata.csv"

# The CSV has two preamble rows (a blank-quoted row and a "Source: ..." note)
# before the real header on line 3.
PREAMBLE_ROWS = 2

# Explicit schema is the contract for the parquet write. Country/year identify
# the row; deciles + mean are monthly real 2005 USD PPP; population is a head
# count (raw persons, ranges from ~750k to ~1.37 billion).
SCHEMA = pa.schema([
    ("country", pa.string()),
    ("year", pa.int32()),
    ("decile_1_income", pa.float64()),
    ("decile_2_income", pa.float64()),
    ("decile_3_income", pa.float64()),
    ("decile_4_income", pa.float64()),
    ("decile_5_income", pa.float64()),
    ("decile_6_income", pa.float64()),
    ("decile_7_income", pa.float64()),
    ("decile_8_income", pa.float64()),
    ("decile_9_income", pa.float64()),
    ("decile_10_income", pa.float64()),
    ("mean_income", pa.float64()),
    ("population", pa.int64()),
])


@transient_retry()
def _fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def fetch_income_deciles(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    text = _fetch_csv(CSV_URL)

    reader = csv.reader(io.StringIO(text))
    all_rows = list(reader)
    header = all_rows[PREAMBLE_ROWS]
    if len(header) != len(SCHEMA):
        raise AssertionError(
            f"unexpected column count: header has {len(header)} cols, "
            f"expected {len(SCHEMA)} ({header})"
        )
    data_rows = all_rows[PREAMBLE_ROWS + 1:]

    countries, years = [], []
    deciles = [[] for _ in range(10)]
    means, pops = [], []
    for row in data_rows:
        if not row or not row[0]:
            continue  # skip any trailing blank lines
        countries.append(row[0])
        years.append(int(row[1]))
        for i in range(10):
            deciles[i].append(float(row[2 + i]))
        means.append(float(row[12]))
        pops.append(int(row[13]))

    columns = [
        pa.array(countries, type=pa.string()),
        pa.array(years, type=pa.int32()),
    ]
    columns += [pa.array(deciles[i], type=pa.float64()) for i in range(10)]
    columns += [
        pa.array(means, type=pa.float64()),
        pa.array(pops, type=pa.int64()),
    ]
    table = pa.Table.from_arrays(columns, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="gcip-gcip-income-deciles", fn=fetch_income_deciles, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="gcip-gcip-income-deciles-transform",
        deps=["gcip-gcip-income-deciles"],
        sql='''
            SELECT
                country,
                CAST(year AS INTEGER)             AS year,
                CAST(decile_1_income  AS DOUBLE)  AS decile_1_income,
                CAST(decile_2_income  AS DOUBLE)  AS decile_2_income,
                CAST(decile_3_income  AS DOUBLE)  AS decile_3_income,
                CAST(decile_4_income  AS DOUBLE)  AS decile_4_income,
                CAST(decile_5_income  AS DOUBLE)  AS decile_5_income,
                CAST(decile_6_income  AS DOUBLE)  AS decile_6_income,
                CAST(decile_7_income  AS DOUBLE)  AS decile_7_income,
                CAST(decile_8_income  AS DOUBLE)  AS decile_8_income,
                CAST(decile_9_income  AS DOUBLE)  AS decile_9_income,
                CAST(decile_10_income AS DOUBLE)  AS decile_10_income,
                CAST(mean_income      AS DOUBLE)  AS mean_income,
                CAST(population       AS BIGINT)  AS population
            FROM "gcip-gcip-income-deciles"
            WHERE country IS NOT NULL AND year IS NOT NULL
        ''',
        key=("country", "year"),
        temporal="year",
    ),
]
