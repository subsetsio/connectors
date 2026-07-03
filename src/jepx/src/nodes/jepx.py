"""JEPX (Japan Electric Power Exchange) — day-ahead (spot) market prices.

Single dataset, single download node. JEPX publishes the spot market as one
Shift-JIS (CP932) CSV per Japanese fiscal year at a stable GET URL:
``https://www.jepx.jp/market/excel/spot_<FY>.csv``. The fiscal year is a
partition, not a schema difference, so the whole corpus is ONE published Delta
table keyed by (delivery_date, slot).

Fetch shape: stateless full re-pull. The corpus is small (~50MB, ~180k rows
across all years) and there is no incremental query parameter, so every run
re-fetches all available fiscal years and overwrites. The current fiscal year's
file grows daily and prior files can carry late corrections; a full re-pull
picks both up for free with no stored watermark to go stale.

Year discovery: start at the verified earliest fiscal year (FY2016 — FY2015 and
earlier 404 on this path) and walk forward, fetching each year until the URL
returns 404, which marks the end of the published range. A safety ceiling raises
rather than looping unboundedly.
"""

import csv
import io
from datetime import datetime, timezone

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

# Verified earliest fiscal year served on the /market/excel/ path.
MIN_FISCAL_YEAR = 2016
SPOT_URL = "https://www.jepx.jp/market/excel/spot_{fy}.csv"

# Core columns by position in the (48-column) CSV. The trailing columns
# (average prices, avoidable cost, block bids, FIP reference prices) are
# omitted; system price + nine area prices + traded volumes are the canonical
# spot dataset. Positions verified against the live header.
#   0 年月日 (delivery date)            1 時刻コード (slot 1-48)
#   2 売り入札量 3 買い入札量 4 約定総量  5 システムプライス
#   6-14 エリアプライス {Hokkaido..Kyushu}
AREA_NAMES = [
    "hokkaido", "tohoku", "tokyo", "chubu", "hokuriku",
    "kansai", "chugoku", "shikoku", "kyushu",
]

SCHEMA = pa.schema(
    [
        ("delivery_date", pa.string()),
        ("slot", pa.int16()),
        ("sell_bid_volume_kwh", pa.float64()),
        ("buy_bid_volume_kwh", pa.float64()),
        ("contract_volume_kwh", pa.float64()),
        ("system_price", pa.float64()),
    ]
    + [(f"area_price_{a}", pa.float64()) for a in AREA_NAMES]
)


def _num(cell: str):
    """Parse a numeric CSV cell; empty/blank → None."""
    cell = cell.strip()
    return float(cell) if cell else None


@transient_retry()
def _fetch_year(fiscal_year: int):
    """Return the decoded CSV text for one fiscal year, or None if that year is
    not published (HTTP 404 = end of range). 5xx/transient errors are retried by
    the decorator; other 4xx raise."""
    resp = get(SPOT_URL.format(fy=fiscal_year), timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.content.decode("cp932")


def fetch_spot(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    # Safety ceiling: a couple of years past the current calendar year. If the
    # walk reaches it without a 404, the source layout changed — raise loudly
    # rather than loop forever.
    max_fiscal_year = datetime.now(tz=timezone.utc).year + 2

    rows: list[dict] = []
    fy = MIN_FISCAL_YEAR
    fetched_years = 0
    while True:
        if fy > max_fiscal_year:
            raise RuntimeError(
                f"reached safety ceiling FY{max_fiscal_year} without a 404 — "
                "JEPX spot URL layout may have changed"
            )
        text = _fetch_year(fy)
        if text is None:
            break  # this fiscal year isn't published yet → end of range
        reader = csv.reader(io.StringIO(text))
        next(reader, None)  # skip header
        for r in reader:
            if len(r) < 15 or not r[0].strip():
                continue
            row = {
                "delivery_date": r[0].strip(),
                "slot": int(r[1]),
                "sell_bid_volume_kwh": _num(r[2]),
                "buy_bid_volume_kwh": _num(r[3]),
                "contract_volume_kwh": _num(r[4]),
                "system_price": _num(r[5]),
            }
            for i, area in enumerate(AREA_NAMES):
                row[f"area_price_{area}"] = _num(r[6 + i])
            rows.append(row)
        fetched_years += 1
        fy += 1

    if fetched_years == 0:
        raise RuntimeError(
            f"no JEPX spot fiscal years fetched starting at FY{MIN_FISCAL_YEAR}"
        )

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="jepx-spot-market", fn=fetch_spot, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="jepx-spot-market-transform",
        deps=["jepx-spot-market"],
        key=("date", "slot"),
        temporal="date",
        sql='''
            SELECT
                strptime(delivery_date, '%Y/%m/%d')::DATE AS date,
                CAST(slot AS INTEGER)                     AS slot,
                CAST(system_price AS DOUBLE)              AS system_price,
                CAST(area_price_hokkaido AS DOUBLE)       AS area_price_hokkaido,
                CAST(area_price_tohoku   AS DOUBLE)       AS area_price_tohoku,
                CAST(area_price_tokyo    AS DOUBLE)       AS area_price_tokyo,
                CAST(area_price_chubu    AS DOUBLE)       AS area_price_chubu,
                CAST(area_price_hokuriku AS DOUBLE)       AS area_price_hokuriku,
                CAST(area_price_kansai   AS DOUBLE)       AS area_price_kansai,
                CAST(area_price_chugoku  AS DOUBLE)       AS area_price_chugoku,
                CAST(area_price_shikoku  AS DOUBLE)       AS area_price_shikoku,
                CAST(area_price_kyushu   AS DOUBLE)       AS area_price_kyushu,
                CAST(sell_bid_volume_kwh AS DOUBLE)       AS sell_bid_volume_kwh,
                CAST(buy_bid_volume_kwh  AS DOUBLE)       AS buy_bid_volume_kwh,
                CAST(contract_volume_kwh AS DOUBLE)       AS contract_volume_kwh
            FROM "jepx-spot-market"
            WHERE delivery_date IS NOT NULL
              AND slot BETWEEN 1 AND 48
            QUALIFY row_number() OVER (PARTITION BY date, slot ORDER BY date) = 1
        ''',
    ),
]
