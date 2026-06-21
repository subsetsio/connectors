"""The Economist — Big Mac Index connector.

Single bulk CSV from the public GitHub repo TheEconomist/big-mac-data. The
`big-mac-full-index.csv` file is a superset of the raw-index and adjusted-index
CSVs (raw PPP indices, GDP-adjusted indices, and the GDP_bigmac per-capita line
value in one file). The whole source is ~2k rows across ~56 countries, dates
2000-04-01 onward, refreshed in place roughly twice a year (Jan/Jul).

Stateless full re-pull: the file is tiny and updated in place, so we re-fetch
the whole corpus every run and overwrite. No watermark/cursor — revisions are
picked up for free. License CC BY-NC-SA 4.0 (The Economist).
"""

import csv
import io

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

FULL_INDEX_URL = (
    "https://raw.githubusercontent.com/TheEconomist/big-mac-data/"
    "master/output-data/big-mac-full-index.csv"
)

# Columns carried through verbatim (lower-cased on the way out). The base
# identification + price columns are always populated; the GDP-adjusted block
# is null for early years (pre-GDP-adjustment), so every numeric column is
# nullable in the raw schema.
_FLOAT_COLS = [
    "local_price",
    "dollar_ex",
    "dollar_price",
    "USD_raw",
    "EUR_raw",
    "GBP_raw",
    "JPY_raw",
    "CNY_raw",
    "GDP_bigmac",
    "adj_price",
    "USD_adjusted",
    "EUR_adjusted",
    "GBP_adjusted",
    "JPY_adjusted",
    "CNY_adjusted",
]

SCHEMA = pa.schema(
    [
        ("date", pa.string()),
        ("iso_a3", pa.string()),
        ("currency_code", pa.string()),
        ("name", pa.string()),
    ]
    + [(c, pa.float64()) for c in _FLOAT_COLS]
)


@transient_retry()
def _fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _parse_float(value):
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    return float(value)


def fetch_big_mac_index(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    text = _fetch_csv(FULL_INDEX_URL)
    reader = csv.DictReader(io.StringIO(text))

    columns = {f.name: [] for f in SCHEMA}
    for row in reader:
        date = (row.get("date") or "").strip()
        if not date:
            continue
        columns["date"].append(date)
        columns["iso_a3"].append((row.get("iso_a3") or "").strip() or None)
        columns["currency_code"].append((row.get("currency_code") or "").strip() or None)
        columns["name"].append((row.get("name") or "").strip() or None)
        for c in _FLOAT_COLS:
            columns[c].append(_parse_float(row.get(c)))

    if not columns["date"]:
        raise ValueError(f"{asset}: parsed 0 rows from {FULL_INDEX_URL}")

    table = pa.table(columns, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="big-mac-economist-big-mac-index",
        fn=fetch_big_mac_index,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="big-mac-economist-big-mac-index-transform",
        deps=["big-mac-economist-big-mac-index"],
        sql='''
            SELECT
                CAST(date AS DATE)         AS date,
                iso_a3,
                currency_code,
                name                       AS country,
                CAST(local_price AS DOUBLE)  AS local_price,
                CAST(dollar_ex AS DOUBLE)    AS dollar_ex,
                CAST(dollar_price AS DOUBLE) AS dollar_price,
                CAST(USD_raw AS DOUBLE)      AS usd_raw,
                CAST(EUR_raw AS DOUBLE)      AS eur_raw,
                CAST(GBP_raw AS DOUBLE)      AS gbp_raw,
                CAST(JPY_raw AS DOUBLE)      AS jpy_raw,
                CAST(CNY_raw AS DOUBLE)      AS cny_raw,
                CAST(GDP_bigmac AS DOUBLE)   AS gdp_per_capita,
                CAST(adj_price AS DOUBLE)    AS adj_price,
                CAST(USD_adjusted AS DOUBLE) AS usd_adjusted,
                CAST(EUR_adjusted AS DOUBLE) AS eur_adjusted,
                CAST(GBP_adjusted AS DOUBLE) AS gbp_adjusted,
                CAST(JPY_adjusted AS DOUBLE) AS jpy_adjusted,
                CAST(CNY_adjusted AS DOUBLE) AS cny_adjusted
            FROM "big-mac-economist-big-mac-index"
            WHERE date IS NOT NULL
              AND iso_a3 IS NOT NULL
              AND dollar_price IS NOT NULL
        ''',
    ),
]
