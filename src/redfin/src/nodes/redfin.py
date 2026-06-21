"""Redfin Data Center — monthly housing market tracker by geography level.

Each geography level is published by Redfin as one gzip-compressed, tab-separated
file on the public S3 bucket `redfin-public-data` (us-west-2), at a stable,
well-known key under `redfin_market_tracker/`. The bucket denies anonymous
LISTing, so the per-level keys are hardcoded (one per rank-accepted entity).

Files are large (national ~0.5MB compressed up to zip ~1.5GB), so the fetch
streams the HTTP body, decompresses and parses the TSV incrementally, keeps only
the ~20 columns the published table needs (dropping the MOM/YOY momentum columns
and internal ids), and writes a streamed Parquet raw asset — all values as
strings. The SqlNodeSpec transform is the typing/cleaning gate: it filters to
"All Residential", non-seasonally-adjusted rows, then casts and renames to a
clean one-row-per-(month, region) table.

Non-seasonally-adjusted (NSA) is used at every level deliberately: Redfin only
publishes seasonally-adjusted series for the ~50 largest metros, so preferring
SA would silently drop ~880 metros (and most other regions). NSA is available
for every region at every level, giving full geographic coverage with one
consistent methodology across all six tables.

Stateless full re-pull: every level file is the complete history and is
overwritten by Redfin on each monthly publish, with no incremental query
surface, so each refresh re-fetches the whole file. Freshness gating is the
maintain step's job.
"""

from __future__ import annotations

import csv
import gzip
import io

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

BASE = "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker"

# spec id -> S3 object key (filename). The bucket can't be listed anonymously,
# so these are hardcoded; they are the rank-accepted entity union.
LEVEL_KEYS = {
    "redfin-market-tracker-national": "us_national_market_tracker.tsv000.gz",
    "redfin-market-tracker-state": "state_market_tracker.tsv000.gz",
    "redfin-market-tracker-metro": "redfin_metro_market_tracker.tsv000.gz",
    "redfin-market-tracker-county": "county_market_tracker.tsv000.gz",
    "redfin-market-tracker-city": "city_market_tracker.tsv000.gz",
    "redfin-market-tracker-zip": "zip_code_market_tracker.tsv000.gz",
}

# Source columns kept in the raw parquet (all stored as strings; the transform
# casts). Order is the parquet schema order.
KEEP_COLS = [
    "PERIOD_BEGIN",
    "REGION_TYPE",
    "REGION",
    "STATE_CODE",
    "PROPERTY_TYPE",
    "IS_SEASONALLY_ADJUSTED",
    "MEDIAN_SALE_PRICE",
    "MEDIAN_LIST_PRICE",
    "MEDIAN_PPSF",
    "MEDIAN_LIST_PPSF",
    "HOMES_SOLD",
    "PENDING_SALES",
    "NEW_LISTINGS",
    "INVENTORY",
    "MONTHS_OF_SUPPLY",
    "MEDIAN_DOM",
    "AVG_SALE_TO_LIST",
    "SOLD_ABOVE_LIST",
    "PRICE_DROPS",
    "OFF_MARKET_IN_TWO_WEEKS",
]

RAW_SCHEMA = pa.schema([(c, pa.string()) for c in KEEP_COLS])
BATCH_ROWS = 200_000


class _StreamReader:
    """Minimal file-like adapter over httpx's byte iterator so gzip can read it."""

    def __init__(self, byte_iter):
        self._it = byte_iter
        self._buf = b""

    def read(self, n: int = -1) -> bytes:
        if n is None or n < 0:
            chunks = [self._buf]
            self._buf = b""
            chunks.extend(self._it)
            return b"".join(chunks)
        while len(self._buf) < n:
            try:
                self._buf += next(self._it)
            except StopIteration:
                break
        out, self._buf = self._buf[:n], self._buf[n:]
        return out


@transient_retry(attempts=5)
def fetch_level(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    key = LEVEL_KEYS[node_id]
    url = f"{BASE}/{key}"

    client = get_client()
    timeout = httpx.Timeout(connect=30.0, read=300.0, write=60.0, pool=60.0)
    with client.stream("GET", url, timeout=timeout) as resp:
        resp.raise_for_status()
        gz = gzip.GzipFile(fileobj=_StreamReader(resp.iter_bytes()))
        text = io.TextIOWrapper(gz, encoding="utf-8", newline="")
        reader = csv.reader(text, delimiter="\t")

        header = next(reader)
        try:
            idx = [header.index(col) for col in KEEP_COLS]
        except ValueError as e:
            raise AssertionError(
                f"{asset}: expected column missing from header ({e}); "
                f"source schema changed"
            )

        with raw_parquet_writer(asset, RAW_SCHEMA) as writer:
            cols: list[list] = [[] for _ in KEEP_COLS]
            n = 0
            total = 0
            for row in reader:
                if len(row) <= idx[-1]:
                    continue  # malformed/short line
                for j, src in enumerate(idx):
                    v = row[src]
                    cols[j].append(v if v != "" else None)
                n += 1
                if n >= BATCH_ROWS:
                    writer.write_batch(
                        pa.record_batch(
                            [pa.array(c, type=pa.string()) for c in cols],
                            schema=RAW_SCHEMA,
                        )
                    )
                    total += n
                    cols = [[] for _ in KEEP_COLS]
                    n = 0
            if n:
                writer.write_batch(
                    pa.record_batch(
                        [pa.array(c, type=pa.string()) for c in cols],
                        schema=RAW_SCHEMA,
                    )
                )
                total += n
            if total == 0:
                raise AssertionError(f"{asset}: parsed 0 data rows from {url}")
            print(f"  {asset}: wrote {total:,} raw rows")


DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fetch_level, kind="download") for sid in LEVEL_KEYS
]


# ---- Transform: one published Delta table per level --------------------------

# raw source column -> clean published column. Each cast to DOUBLE.
_VALUE_MAP = [
    ("MEDIAN_SALE_PRICE", "median_sale_price"),
    ("MEDIAN_LIST_PRICE", "median_list_price"),
    ("MEDIAN_PPSF", "median_price_per_sqft"),
    ("MEDIAN_LIST_PPSF", "median_list_price_per_sqft"),
    ("HOMES_SOLD", "homes_sold"),
    ("PENDING_SALES", "pending_sales"),
    ("NEW_LISTINGS", "new_listings"),
    ("INVENTORY", "inventory"),
    ("MONTHS_OF_SUPPLY", "months_of_supply"),
    ("MEDIAN_DOM", "median_days_on_market"),
    ("AVG_SALE_TO_LIST", "avg_sale_to_list_ratio"),
    ("SOLD_ABOVE_LIST", "pct_sold_above_list"),
    ("PRICE_DROPS", "pct_price_drops"),
    ("OFF_MARKET_IN_TWO_WEEKS", "pct_off_market_two_weeks"),
]


def _market_sql(dep_id: str, national: bool) -> str:
    value_select = ",\n            ".join(
        f"TRY_CAST({src} AS DOUBLE) AS {dst}" for src, dst in _VALUE_MAP
    )
    value_any = ", ".join(dst for _, dst in _VALUE_MAP)
    region_cols = "TRIM(REGION) AS region_name"
    if not national:
        region_cols += ",\n            NULLIF(TRIM(STATE_CODE), '') AS state_code"
    partition = "date" if national else "date, region_name"
    return f'''
        WITH sel AS (
            SELECT
                CAST(PERIOD_BEGIN AS DATE) AS date,
                {region_cols},
                {value_select}
            FROM "{dep_id}"
            WHERE TRIM(PROPERTY_TYPE) = 'All Residential'
              AND lower(IS_SEASONALLY_ADJUSTED) IN ('false', 'f', '0')
        )
        SELECT * FROM sel
        WHERE coalesce({value_any}) IS NOT NULL
        QUALIFY row_number() OVER (PARTITION BY {partition} ORDER BY region_name) = 1
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_market_sql(s.id, national=s.id.endswith("-national")),
    )
    for s in DOWNLOAD_SPECS
]
