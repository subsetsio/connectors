"""AEMO — NEM aggregated price and demand.

One published subset: 5-minute (30-minute pre-2021) regional settlement
observations of demand and wholesale price for the National Electricity
Market. Source is the bulk_priceanddemand mechanism: one stable CSV per
(region, calendar month) at
https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_<YYYYMM>_<REGION>.csv

Fetch shape: stateless full re-pull (shape 1). The corpus is bounded
(~6 regions x ~330 months, a few hundred MB of CSV) and there is no
query-level delta filter — the per-(region,month) partitioning is the only
incremental unit, and historical months are immutable. We re-enumerate every
(region, month) from the source's documented start (1998-12) to the current
month each run and stream them into one parquet asset; closed-month files are
identical run-to-run, the open month is picked up for free. Memory stays
bounded because we parse and flush one monthly CSV at a time via the streaming
parquet writer. A 404 means "not published for this (region, month)" (e.g.
SNOWY1 after 2008, TAS1 before 2005) and is skipped, not an error.
"""

import csv
import io
from datetime import datetime, timezone

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)

# NEM regions. NSW1/QLD1/VIC1/SA1 from market start; TAS1 from 2005; SNOWY1 was
# a distinct region until its abolition in 2008 (historical files only).
REGIONS = ["NSW1", "QLD1", "VIC1", "SA1", "TAS1", "SNOWY1"]

# Documented earliest month of the aggregated product.
SOURCE_MIN_YEAR = 1998
SOURCE_MIN_MONTH = 12

BASE_URL = "https://aemo.com.au/aemo/data/nem/priceanddemand"

SCHEMA = pa.schema([
    ("region", pa.string()),
    ("settlement_date", pa.timestamp("s")),
    ("total_demand", pa.float64()),
    ("rrp", pa.float64()),
    ("period_type", pa.string()),
])


def _months(start_year, start_month):
    """Yield (YYYYMM string) from the start month through the current month."""
    now = datetime.now(tz=timezone.utc)
    y, m = start_year, start_month
    while (y, m) <= (now.year, now.month):
        yield f"{y:04d}{m:02d}"
        m += 1
        if m > 12:
            m = 1
            y += 1


def _parse_settlement_date(s):
    """AEMO uses 'YYYY/MM/DD HH:MM:SS' (5-min era) and 'YYYY/MM/DD HH:MM'
    (30-min era, no seconds). Try both."""
    s = s.strip()
    for fmt in ("%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"unparseable SETTLEMENTDATE: {s!r}")


@transient_retry()
def _fetch_csv(url):
    """Return the CSV text, or None if the (region, month) is not published.

    raise_for_status() inside the retried body lets transient_retry handle
    429/5xx/network errors; a 404 is permanent (not-yet-published / region
    didn't exist that month) and returns None cleanly without raising."""
    resp = get(url, timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.text


def _parse_month(text):
    """Parse one monthly CSV into a pyarrow Table conforming to SCHEMA."""
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    expected = ["REGION", "SETTLEMENTDATE", "TOTALDEMAND", "RRP", "PERIODTYPE"]
    if [h.strip().upper() for h in header] != expected:
        raise ValueError(f"unexpected CSV header: {header!r}")

    regions, dates, demands, rrps, ptypes = [], [], [], [], []
    for row in reader:
        if not row or not row[0].strip():
            continue
        regions.append(row[0].strip())
        dates.append(_parse_settlement_date(row[1]))
        demands.append(float(row[2]) if row[2].strip() else None)
        rrps.append(float(row[3]) if row[3].strip() else None)
        ptypes.append(row[4].strip() if len(row) > 4 else None)

    return pa.table(
        {
            "region": pa.array(regions, pa.string()),
            "settlement_date": pa.array(dates, pa.timestamp("s")),
            "total_demand": pa.array(demands, pa.float64()),
            "rrp": pa.array(rrps, pa.float64()),
            "period_type": pa.array(ptypes, pa.string()),
        },
        schema=SCHEMA,
    )


def fetch_price_and_demand(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    months = list(_months(SOURCE_MIN_YEAR, SOURCE_MIN_MONTH))
    written = 0
    with raw_parquet_writer(asset, SCHEMA) as writer:
        for region in REGIONS:
            for ym in months:
                url = f"{BASE_URL}/PRICE_AND_DEMAND_{ym}_{region}.csv"
                text = _fetch_csv(url)
                if text is None:
                    continue
                table = _parse_month(text)
                if table.num_rows == 0:
                    continue
                writer.write_table(table)
                written += 1
    if written == 0:
        raise RuntimeError(
            "no (region, month) CSVs fetched — source layout or URL pattern "
            "may have changed"
        )


DOWNLOAD_SPECS = [
    NodeSpec(
        id="australian-energy-market-operator-price-and-demand",
        fn=fetch_price_and_demand,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="australian-energy-market-operator-price-and-demand-transform",
        deps=["australian-energy-market-operator-price-and-demand"],
        sql='''
            SELECT
                region,
                settlement_date,
                total_demand,
                rrp,
                period_type
            FROM "australian-energy-market-operator-price-and-demand"
            WHERE region IS NOT NULL
              AND settlement_date IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY region, settlement_date
                ORDER BY total_demand DESC NULLS LAST
            ) = 1
        ''',
    ),
]
