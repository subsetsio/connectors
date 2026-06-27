"""National Bank of Kazakhstan — official daily foreign-exchange rates.

Mechanism (from research, id `rest_rates_xml`): the per-date RSS/XML endpoint
`https://nationalbank.kz/rss/get_rates.cfm?fdate=DD.MM.YYYY`. Each request returns
the complete all-currency snapshot (KZT per `quant` units of each currency) for one
calendar date. There is no bulk/range export, so the full history is built by
iterating one HTTP request per calendar date.

Shape: stateless full re-pull. Each run re-fetches the whole history — every year
from SOURCE_MIN_YEAR to today — and overwrites. Raw is run-scoped (each run starts
with an empty raw dir), so cross-run state/skip logic would silently drop history;
a full re-pull is the only correct shape here, and it also picks up any source
revisions for free. The corpus is small (~331k rows / ~2MB) but spans ~9700 dates,
so raw is written one batch per year (`national-bank-fx-rates-<year>`) to bound
memory; the SQL transform glob-unions all year batches.
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
import xml.etree.ElementTree as ET

# Documented floor: the get_rates.cfm feed returns data from late 1999 onward
# (probed: 1997-1998 empty; 15.12.1999 onward populated). Earlier dates return an
# empty <rates> document and are skipped. The end of the range is discovered at
# run time (today), never hardcoded.
SOURCE_MIN_YEAR = 1999

# Modest concurrency for the per-date fan-out within a single year. The source
# documents no rate limit and none was observed during probing.
_FETCH_WORKERS = 8

_BASE_URL = "https://nationalbank.kz/rss/get_rates.cfm"

SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("currency_code", pa.string()),
    ("currency_name", pa.string()),
    ("rate", pa.float64()),
    ("quant", pa.int64()),
    ("change", pa.float64()),
    ("direction", pa.string()),
])


@transient_retry()  # 6 attempts, exponential backoff; retries 429/5xx/transient net errors
def _fetch_date_xml(fdate: str) -> bytes:
    resp = get(_BASE_URL, params={"fdate": fdate}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _parse_float(text: str):
    text = (text or "").strip().replace("+", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _fetch_one_day(d: date) -> list[dict]:
    """Fetch and parse one date's all-currency snapshot. Empty list when the
    source has no publication for that date (weekends/holidays/pre-history)."""
    fdate = d.strftime("%d.%m.%Y")
    root = ET.fromstring(_fetch_date_xml(fdate))
    rows = []
    for item in root.findall(".//item"):
        code = (item.findtext("title") or "").strip()
        if not code:
            continue
        rate = _parse_float(item.findtext("description"))
        quant_text = (item.findtext("quant") or "").strip()
        try:
            quant = int(quant_text) if quant_text else None
        except ValueError:
            quant = None
        direction = (item.findtext("index") or "").strip() or None
        rows.append({
            "date": d,
            "currency_code": code,
            "currency_name": (item.findtext("fullname") or "").strip() or None,
            "rate": rate,
            "quant": quant,
            "change": _parse_float(item.findtext("change")),
            "direction": direction,
        })
    return rows


def _fetch_year(year: int, end: date) -> list[dict]:
    """All daily snapshots for `year`, up to and including `end`."""
    start = date(year, 1, 1)
    last = min(date(year, 12, 31), end)
    days = []
    d = start
    while d <= last:
        days.append(d)
        d += timedelta(days=1)

    rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=_FETCH_WORKERS) as pool:
        for day_rows in pool.map(_fetch_one_day, days):
            rows.extend(day_rows)
    return rows


def fetch_fx_rates(node_id: str) -> None:
    asset_base = node_id  # "national-bank-fx-rates"

    today = datetime.now(tz=timezone.utc).date()  # frozen for this run
    current_year = today.year

    # Full re-pull every run: every year is fetched and its batch overwritten.
    # Raw is run-scoped, so there is nothing to resume from across runs.
    for year in range(SOURCE_MIN_YEAR, current_year + 1):
        rows = _fetch_year(year, today)
        if rows:
            table = pa.Table.from_pylist(rows, schema=SCHEMA)
            save_raw_parquet(table, f"{asset_base}-{year}")


DOWNLOAD_SPECS = [
    NodeSpec(id="national-bank-fx-rates", fn=fetch_fx_rates, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="national-bank-fx-rates-transform",
        deps=["national-bank-fx-rates"],
        sql='''
            SELECT
                CAST(date AS DATE)            AS date,
                currency_code,
                currency_name,
                CAST(rate AS DOUBLE)          AS rate,
                CAST(quant AS BIGINT)         AS quant,
                CAST(rate AS DOUBLE) / NULLIF(CAST(quant AS DOUBLE), 0) AS rate_per_unit,
                CAST(change AS DOUBLE)        AS change,
                direction
            FROM "national-bank-fx-rates"
            WHERE rate IS NOT NULL
              AND rate > 0                 -- drop meaningless 0 rates (e.g. LTL at 2015 euro changeover)
              AND quant IS NOT NULL
              AND currency_code IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY date, currency_code ORDER BY rate
            ) = 1
        ''',
    ),
]
