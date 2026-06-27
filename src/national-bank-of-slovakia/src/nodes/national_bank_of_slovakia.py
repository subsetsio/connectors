"""National Bank of Slovakia (NBS) — exchange-rate connector.

NBS's only first-party machine-readable surface is the per-period exchange-rate
export at https://nbs.sk/export/en/... There is no bulk/range endpoint: each URL
returns exactly one period's document, so building the full history means walking
the period axis (one request per business day for the daily feed, one per month
for the foreign feed).

Two subsets, each fetched as a **yearly firehose**:

  * exchange-rate-daily          — ECB EUR reference rates NBS republishes, ~30
    currencies, daily on TARGET working days, history back to 1999.
  * exchange-rate-foreign-monthly — NBS "selected foreign currencies" vs EUR,
    ~130-150 currencies, monthly, history back to 1996.

Why a firehose and not a stateless full re-pull: the daily feed alone is ~7000
business-day documents. Re-fetching all of them on every refresh would be both
slow and rude to a public government endpoint. Instead raw is written one parquet
**batch per year** (`<spec-id>-<year>`); closed (past) years are immutable and
fetched once (tracked in state), and only the open current year is re-pulled each
refresh. The SQL transform globs `<spec-id>-*` so every year batch unions back
together. State holds only the set of completed closed years — a monotonic
watermark, never a terminal flag.

The daily export returns the rate effective *on or before* the requested date
(weekends/holidays echo the preceding business day, with the true date inside the
document), so we key by the document's own date to dedup; the transform applies a
final per-(date, currency) dedup as a safety net.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    load_state,
    save_state,
)

STATE_VERSION = 1
BASE = "https://nbs.sk/export/en"

# Source facts (the start of each series). The *end* is always discovered from
# the wall clock — never hardcoded — so the connector never goes stale.
EARLIEST_DAILY_YEAR = 1999      # ECB euro reference rates begin 1999-01-04
EARLIEST_FOREIGN_YEAR = 1996    # NBS selected-foreign-currency rates begin 1996

# Modest concurrency for the per-day daily backfill — nbs.sk documents no rate
# limit and served probes instantly; 8 workers keeps us polite.
_DAILY_WORKERS = 8

DAILY_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("currency", pa.string()),
    ("rate", pa.float64()),
])

FOREIGN_SCHEMA = pa.schema([
    ("valid_from", pa.date32()),
    ("country", pa.string()),
    ("currency_code", pa.string()),
    ("currency_name", pa.string()),
    ("value", pa.float64()),
])

_FOREIGN_NS = {"n": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def _today() -> date:
    return datetime.now(tz=timezone.utc).date()


@transient_retry()
def _fetch(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _to_float(token: str) -> float:
    # NBS uses '.' as decimal and ',' as a thousands separator (e.g. "16,872.43").
    return float(token.replace(",", ""))


# --- daily (ECB reference rates) -------------------------------------------

def _parse_daily_csv(text: str):
    """Return (effective_date, {currency: rate}) or None for an empty document."""
    text = text.lstrip("﻿").strip()
    if not text:
        return None
    lines = text.splitlines()
    if len(lines) < 2:
        return None
    header = [h.strip() for h in lines[0].split(";")]
    values = [v.strip() for v in lines[1].split(";")]
    if not values or not values[0]:
        return None
    day, month, year = values[0].split(".")
    eff = date(int(year), int(month), int(day))
    rates: dict[str, float] = {}
    for i in range(1, len(header)):
        if i >= len(values):
            break
        cur, raw = header[i], values[i]
        if cur and raw:
            rates[cur] = _to_float(raw)
    return eff, rates


def _fetch_daily_day(d: date):
    resp = _fetch(f"{BASE}/exchange-rate/{d.isoformat()}/csv")
    return _parse_daily_csv(resp.text)


def _fetch_daily_year(year: int) -> list[dict]:
    """Fetch every business day of `year` (up to today) concurrently and dedup by
    the document's own effective date (holidays/weekends echo the prior day)."""
    start = date(year, 1, 1)
    end = min(date(year, 12, 31), _today())
    days = []
    d = start
    while d <= end:
        if d.weekday() < 5:  # Mon-Fri
            days.append(d)
        d += timedelta(days=1)
    if not days:
        return []

    by_date: dict[date, dict[str, float]] = {}
    with ThreadPoolExecutor(max_workers=_DAILY_WORKERS) as pool:
        for parsed in pool.map(_fetch_daily_day, days):
            if parsed is None:
                continue
            eff, rates = parsed
            by_date[eff] = rates  # identical echoes collapse onto the same date

    rows = []
    for eff, rates in by_date.items():
        for cur, rate in rates.items():
            rows.append({"date": eff, "currency": cur, "rate": rate})
    return rows


# --- foreign (selected foreign currencies, monthly) ------------------------

def _parse_foreign_xml(content: bytes) -> list[dict]:
    root = ET.fromstring(content)
    vf = root.findtext("n:validFrom", namespaces=_FOREIGN_NS)
    valid_from = date.fromisoformat(vf) if vf else None
    rows = []
    for rt in root.iterfind(".//n:rate", _FOREIGN_NS):
        code = rt.findtext("n:ccyCode", namespaces=_FOREIGN_NS)
        val = rt.findtext("n:value", namespaces=_FOREIGN_NS)
        if not code or not val or not val.strip():
            continue
        rows.append({
            "valid_from": valid_from,
            "country": rt.findtext("n:country", namespaces=_FOREIGN_NS),
            "currency_code": code,
            "currency_name": rt.findtext("n:currency", namespaces=_FOREIGN_NS),
            "value": _to_float(val),
        })
    return rows


def _fetch_foreign_year(year: int) -> list[dict]:
    """Fetch each month of `year` (up to the current month). Out-of-range / not-yet
    -published months return a document with an empty rate list, which yields []."""
    last_month = 12
    today = _today()
    if year == today.year:
        last_month = today.month
    rows: list[dict] = []
    for month in range(1, last_month + 1):
        resp = _fetch(f"{BASE}/exchange-rate-foreign/{year}-{month:02d}/xml")
        if not resp.content.strip():
            continue
        rows.extend(_parse_foreign_xml(resp.content))
    return rows


# --- shared yearly-firehose driver -----------------------------------------

def _run_yearly_firehose(node_id, earliest_year, year_fetcher, schema):
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION, "completed_years": []}
    completed = set(state.get("completed_years", []))
    current_year = _today().year

    for year in range(earliest_year, current_year + 1):
        closed = year < current_year
        if closed and year in completed:
            continue  # immutable, already fetched
        rows = year_fetcher(year)
        if rows:
            table = pa.Table.from_pylist(rows, schema=schema)
            save_raw_parquet(table, f"{node_id}-{year}")  # raw before state
        if closed:
            completed.add(year)
            save_state(node_id, {
                "schema_version": STATE_VERSION,
                "completed_years": sorted(completed),
            })


def fetch_exchange_rate_daily(node_id: str) -> None:
    _run_yearly_firehose(node_id, EARLIEST_DAILY_YEAR, _fetch_daily_year, DAILY_SCHEMA)


def fetch_exchange_rate_foreign_monthly(node_id: str) -> None:
    _run_yearly_firehose(node_id, EARLIEST_FOREIGN_YEAR, _fetch_foreign_year, FOREIGN_SCHEMA)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="national-bank-of-slovakia-exchange-rate-daily",
        fn=fetch_exchange_rate_daily,
        kind="download",
    ),
    NodeSpec(
        id="national-bank-of-slovakia-exchange-rate-foreign-monthly",
        fn=fetch_exchange_rate_foreign_monthly,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="national-bank-of-slovakia-exchange-rate-daily-transform",
        deps=["national-bank-of-slovakia-exchange-rate-daily"],
        sql='''
            SELECT date, currency_code, rate
            FROM (
                SELECT
                    CAST(date AS DATE)     AS date,
                    currency               AS currency_code,
                    CAST(rate AS DOUBLE)   AS rate,
                    row_number() OVER (
                        PARTITION BY date, currency ORDER BY rate DESC
                    ) AS rn
                FROM "national-bank-of-slovakia-exchange-rate-daily"
                WHERE rate IS NOT NULL
            )
            WHERE rn = 1
        ''',
    ),
    SqlNodeSpec(
        id="national-bank-of-slovakia-exchange-rate-foreign-monthly-transform",
        deps=["national-bank-of-slovakia-exchange-rate-foreign-monthly"],
        sql='''
            SELECT valid_from, currency_code, country, currency_name, value
            FROM (
                SELECT
                    CAST(valid_from AS DATE) AS valid_from,
                    currency_code,
                    country,
                    currency_name,
                    CAST(value AS DOUBLE)    AS value,
                    row_number() OVER (
                        PARTITION BY valid_from, currency_code ORDER BY value DESC
                    ) AS rn
                FROM "national-bank-of-slovakia-exchange-rate-foreign-monthly"
                WHERE value IS NOT NULL
            )
            WHERE rn = 1
        ''',
    ),
]
