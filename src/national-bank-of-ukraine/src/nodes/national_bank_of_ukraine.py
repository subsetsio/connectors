"""National Bank of Ukraine (NBU) connector.

Mechanism: the NBUStatService REST API (`/NBUStatService/v1/statdirectory/<mnemonic>?json`),
plus the dedicated NBU_Exchange/exchange_site service for official FX rates. All
requests must carry a browser User-Agent — bank.gov.ua is behind Cloudflare,
which 403s default library UAs.

One published Delta table per dataset mnemonic. Each statdirectory dataset is a
long-format table sharing the schema {dt, id_api, txt/txten, freq, value} plus
dataset-specific dimension columns; individual series differ only by id_api /
dimension values (columns within the table).

Three fetch strategies, dispatched per entity:

* FULL  — `<mnemonic>?json` returns the entire history in one request. Stateless
          full re-pull each run (overwrite). Used for the 21 datasets whose
          no-parameter call succeeds.
* WINDOWED — the 7 datasets whose no-parameter call returns HTTP 400 "too large"
          (balanceofpayments, banksfinrep, deposit, inflation, kursf, loan via
          start/end; mir via period=m). These are large and the source supports
          month-windowed querying, so we fetch incrementally: month-by-month
          batches, resuming from a saved watermark and re-fetching the most
          recent OVERLAP_MONTHS each run to absorb revisions. Backfill is a
          sequence of supervisor-bounded refreshes.
* EXCHANGE_SITE — official-exchange-rates: FX history (back to 1996) via
          exchange_site, one year per request (multi-year ranges truncate);
          incremental by year with a one-year overlap.

No documented or observed rate limit (Cloudflare-cached); modest concurrency.
"""

from __future__ import annotations

import calendar
from datetime import datetime, timezone

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
    load_state,
    save_state,
)
from constants import ENTITY_IDS

SLUG = "national-bank-of-ukraine"
STATDIR = "https://bank.gov.ua/NBUStatService/v1/statdirectory/"
EXCHANGE_SITE = "https://bank.gov.ua/NBU_Exchange/exchange_site"
# Cloudflare 403s default library UAs; a browser UA is mandatory. ASCII only.
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
HEADERS = {"User-Agent": UA, "Accept": "application/json"}

STATE_VERSION = 1
OVERLAP_MONTHS = 2          # re-fetch recent months each refresh (revision lag)
OVERLAP_YEARS = 1           # FX: re-fetch current + prior year each refresh
SOURCE_FLOOR_MONTH = "199601"   # absolute lower bound; empty leading months skipped
FX_FLOOR_YEAR = 1996            # earliest FX history observed on exchange_site

# Fetch-strategy classification by statdirectory mnemonic. NOT the coverage list
# (that is ENTITY_IDS) — just HOW each non-default dataset is windowed. Anything
# not listed here uses the FULL no-parameter strategy.
WINDOW_START_END = {"balanceofpayments", "banksfinrep", "deposit", "inflation", "kursf", "loan"}
WINDOW_PERIOD_M = {"mir"}


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
@transient_retry()
def _get_json(url: str) -> list:
    """GET a statdirectory / exchange_site JSON array. Raises on non-list
    payloads (error envelopes come back as 4xx and raise via raise_for_status;
    a 200 object/truncated body is a real problem, surfaced loudly)."""
    resp = get(url, headers=HEADERS, timeout=(10.0, 180.0))
    resp.raise_for_status()
    body = resp.text.lstrip()
    if not body:
        return []
    if not body.startswith("["):
        raise RuntimeError(f"expected JSON array from {url}; got: {resp.text[:200]!r}")
    return resp.json()


# --------------------------------------------------------------------------- #
# Month helpers
# --------------------------------------------------------------------------- #
def _month_index(ym: str) -> int:
    return int(ym[:4]) * 12 + (int(ym[4:6]) - 1)


def _ym_from_index(idx: int) -> str:
    return f"{idx // 12:04d}{idx % 12 + 1:02d}"


def _month_add(ym: str, delta: int) -> str:
    return _ym_from_index(_month_index(ym) + delta)


def _month_iter(start_ym: str, end_ym: str):
    for idx in range(_month_index(start_ym), _month_index(end_ym) + 1):
        yield _ym_from_index(idx)


def _current_ym() -> str:
    now = datetime.now(timezone.utc)
    return f"{now.year:04d}{now.month:02d}"


# --------------------------------------------------------------------------- #
# Fetch strategies
# --------------------------------------------------------------------------- #
def _fetch_full(node_id: str, mnemonic: str) -> None:
    """Whole history in one request; overwrite the single raw asset."""
    rows = _get_json(f"{STATDIR}{mnemonic}?json")
    if not rows:
        raise RuntimeError(f"{mnemonic}: full-history response was empty")
    save_raw_ndjson(rows, node_id)


def _fetch_month(mnemonic: str, ym: str) -> list:
    if mnemonic in WINDOW_PERIOD_M:
        return _get_json(f"{STATDIR}{mnemonic}?period=m&date={ym}&json")
    # start/end inclusive over the whole calendar month
    year, month = int(ym[:4]), int(ym[4:6])
    last_day = calendar.monthrange(year, month)[1]
    return _get_json(f"{STATDIR}{mnemonic}?start={ym}01&end={ym}{last_day:02d}&json")


def _fetch_windowed(node_id: str, mnemonic: str) -> None:
    """Incremental month-by-month batching with a watermark."""
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark = state.get("watermark")  # last month processed, "YYYYMM"
    start_ym = _month_add(watermark, -OVERLAP_MONTHS) if watermark else SOURCE_FLOOR_MONTH
    if _month_index(start_ym) < _month_index(SOURCE_FLOOR_MONTH):
        start_ym = SOURCE_FLOOR_MONTH
    current_ym = _current_ym()

    for ym in _month_iter(start_ym, current_ym):
        rows = _fetch_month(mnemonic, ym)
        if rows:
            save_raw_ndjson(rows, f"{node_id}-{ym}")  # write raw FIRST
        save_state(node_id, {"schema_version": STATE_VERSION, "watermark": ym})


def _fetch_exchange_site(node_id: str) -> None:
    """Official FX rates, one year per request; incremental by year."""
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark = state.get("watermark")  # last year processed (int)
    start_year = max(FX_FLOOR_YEAR, int(watermark) - OVERLAP_YEARS) if watermark else FX_FLOOR_YEAR
    current_year = datetime.now(timezone.utc).year

    for year in range(start_year, current_year + 1):
        rows = _get_json(f"{EXCHANGE_SITE}?start={year}0101&end={year}1231&json")
        if rows:
            save_raw_ndjson(rows, f"{node_id}-{year}")  # write raw FIRST
        save_state(node_id, {"schema_version": STATE_VERSION, "watermark": year})


def fetch_one(node_id: str) -> None:
    """Single entry point for every download node. Recovers the dataset from the
    spec id and dispatches to the right strategy."""
    suffix = node_id[len(SLUG) + 1:]
    if suffix == "official-exchange-rates":
        _fetch_exchange_site(node_id)
    elif suffix in WINDOW_START_END or suffix in WINDOW_PERIOD_M:
        _fetch_windowed(node_id, suffix)
    else:
        _fetch_full(node_id, suffix)


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #
def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


def _statdir_transform_sql(dep_id: str) -> str:
    # Long-format statistics table. Common typed columns + every dataset-specific
    # dimension column preserved verbatim. DISTINCT collapses overlap duplicates
    # produced by the windowed re-fetch.
    return f'''
        SELECT DISTINCT
            strptime(CAST(dt AS VARCHAR), '%Y%m%d')::DATE AS date,
            CAST(id_api AS VARCHAR)  AS series_id,
            CAST(txten AS VARCHAR)   AS series_name_en,
            CAST(txt AS VARCHAR)     AS series_name_uk,
            CAST(freq AS VARCHAR)    AS frequency,
            TRY_CAST(value AS DOUBLE) AS value,
            * EXCLUDE (dt, id_api, txten, txt, freq, value)
        FROM "{dep_id}"
        WHERE dt IS NOT NULL
          AND value IS NOT NULL
          AND TRY_CAST(value AS DOUBLE) IS NOT NULL
    '''


def _fx_transform_sql(dep_id: str) -> str:
    # Official UAH exchange rates. exchangedate / calcdate are DD.MM.YYYY;
    # calcdate is sometimes blank for early records.
    return f'''
        SELECT DISTINCT
            strptime(CAST(exchangedate AS VARCHAR), '%d.%m.%Y')::DATE AS date,
            CAST(cc AS VARCHAR)              AS currency_code,
            TRY_CAST(r030 AS INTEGER)       AS currency_numeric_code,
            CAST(enname AS VARCHAR)         AS currency_name_en,
            CAST(txt AS VARCHAR)            AS currency_name_uk,
            TRY_CAST(rate AS DOUBLE)        AS rate,
            TRY_CAST(units AS INTEGER)      AS units,
            TRY_CAST(rate_per_unit AS DOUBLE) AS rate_per_unit,
            CAST("group" AS VARCHAR)        AS currency_group,
            CASE
                WHEN trim(CAST(calcdate AS VARCHAR)) = '' THEN NULL
                ELSE strptime(trim(CAST(calcdate AS VARCHAR)), '%d.%m.%Y')::DATE
            END AS calc_date
        FROM "{dep_id}"
        WHERE exchangedate IS NOT NULL
          AND TRY_CAST(rate AS DOUBLE) IS NOT NULL
    '''


def _transform_for(dep_id: str) -> SqlNodeSpec:
    suffix = dep_id[len(SLUG) + 1:]
    sql = _fx_transform_sql(dep_id) if suffix == "official-exchange-rates" else _statdir_transform_sql(dep_id)
    return SqlNodeSpec(id=f"{dep_id}-transform", deps=[dep_id], sql=sql)


TRANSFORM_SPECS = [_transform_for(s.id) for s in DOWNLOAD_SPECS]
