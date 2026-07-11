"""National Bank of Ukraine (NBU) connector — raw downloads.

Mechanism: the NBUStatService REST API
(`/NBUStatService/v1/statdirectory/<mnemonic>?json`) plus the dedicated
`NBU_Exchange/exchange_site` service for official FX rates. Every request must
carry a browser User-Agent — bank.gov.ua sits behind Cloudflare, which 403s
default library UAs.

One published Delta table per dataset (one raw asset per download node). Each
statdirectory dataset is a long-format table sharing the common columns
{dt, id_api, txt/txten, freq, value} plus dataset-specific dimension columns;
individual series differ only by id_api / dimension *values* (columns within the
table). Raw is written as NDJSON — records are heterogeneous across datasets and
carry drifting dimension keys, so a fixed parquet schema would be brittle.

Fetch dispatch, per dataset:

* FULL — `<mnemonic>?json` returns the entire history in one request. Stateless
  full re-pull each run (single asset, overwrite). Used for every dataset whose
  no-parameter call succeeds (~34 of them).
* WINDOWED (adaptive year -> month) — datasets whose no-parameter call returns
  HTTP 400 "dataset too large". We fetch a year at a time via start/end; if a
  single year is itself too large, that year is split into calendar months.
  Each written window is a raw *fragment* of the one logical asset (the
  transform's dep view spans all fragments). Incremental by year with a
  one-year overlap to absorb revisions; a persisted watermark makes backfill a
  sequence of supervisor-bounded refreshes.
* FORCE-MONTH — `mir` is ~51k rows *per month* (~20 MB); a year would be far too
  large, so it skips the year attempt and windows straight to months.
* EXCHANGE_SITE — `official-exchange-rates`: FX history via exchange_site, one
  year per request (multi-year ranges truncate); incremental by year, one-year
  overlap.

The catalog's `apikod` for two datasets differs from the actual endpoint path
segment (`cashflow` -> `casflow`, `q_survey` -> `qsurvey`); MNEMONIC maps them.

No documented or observed rate limit (Cloudflare-cached); modest concurrency.
"""

from __future__ import annotations

import calendar
from datetime import datetime, timezone

from subsets_utils import (
    NodeSpec,
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
OVERLAP_YEARS = 1               # re-fetch current + prior year each refresh
DEFAULT_FLOOR_YEAR = 2000       # windowing lower bound when no entrydate is known
FX_FLOOR_YEAR = 1996            # earliest FX history observed on exchange_site

# Catalog apikod -> actual statdirectory endpoint segment, where they differ.
MNEMONIC = {"cashflow": "casflow", "q_survey": "qsurvey"}

# Datasets that must window straight to months (a year window is itself too big).
FORCE_MONTH = {"mir"}

# Windowing lower bound per dataset, from the catalog's `entrydate`. Only the
# datasets that actually need windowing (their full call returns 400) are
# listed; everything else fetches full and never consults this.
FLOOR_YEAR = {
    "balanceofpayments": 2009,
    "inflation": 2007,
    "klk": 2017,
    "kursf": 2012,
    "sklrk": 2018,
    "emd": 1996,
    "mir": 2010,
    "banksfinrep": 2012,
    "deposit": 2010,
    "loan": 2010,
    "osb": 2017,
}


def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# spec id -> original entity id (reverses the id transform without guessing).
SPEC_ENTITY = {_spec_id(eid): eid for eid in ENTITY_IDS}


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
class _TooLarge(Exception):
    """NBUStatService returned 400 'dataset too large' — the query must be
    narrowed by a start/end (or period) window and retried."""


@transient_retry()
def _get_rows(url: str) -> list:
    """GET a statdirectory / exchange_site JSON array.

    A 400 is the API's 'dataset too large' signal (raised as _TooLarge for the
    caller to window). Any other non-2xx raises via raise_for_status. A 200 that
    isn't a JSON array is a real problem and is surfaced loudly.
    """
    resp = get(url, headers=HEADERS, timeout=(10.0, 180.0))
    if resp.status_code == 400:
        raise _TooLarge(url)
    resp.raise_for_status()
    body = resp.text.lstrip()
    if not body:
        return []
    if not body.startswith("["):
        raise RuntimeError(f"expected JSON array from {url}; got: {resp.text[:200]!r}")
    return resp.json()


def _range_url(mnemonic: str, start: str, end: str) -> str:
    return f"{STATDIR}{mnemonic}?start={start}&end={end}&json"


# --------------------------------------------------------------------------- #
# Fetch strategies
# --------------------------------------------------------------------------- #
def _fetch_full(node_id: str, mnemonic: str) -> None:
    """Whole history in one request; overwrite the single raw asset."""
    rows = _get_rows(f"{STATDIR}{mnemonic}?json")
    if not rows:
        raise RuntimeError(f"{mnemonic}: full-history response was empty")
    save_raw_ndjson(rows, node_id)


def _fetch_year_by_month(node_id: str, mnemonic: str, year: int) -> None:
    """Fetch one calendar year split into 12 month windows, one fragment each."""
    for month in range(1, 13):
        last = calendar.monthrange(year, month)[1]
        start = f"{year:04d}{month:02d}01"
        end = f"{year:04d}{month:02d}{last:02d}"
        rows = _get_rows(_range_url(mnemonic, start, end))
        if rows:
            save_raw_ndjson(rows, node_id, fragment=f"{year:04d}{month:02d}")


def _fetch_windowed(node_id: str, mnemonic: str, *, force_month: bool) -> None:
    """Incremental year-by-year windowing with a persisted watermark.

    Each year is fetched as a single start/end window; a year that is itself too
    large is split into months. force_month skips the year attempt entirely.
    """
    entity = SPEC_ENTITY[node_id]
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    floor = FLOOR_YEAR.get(entity, DEFAULT_FLOOR_YEAR)
    watermark = state.get("watermark")  # last year processed (int)
    start_year = max(floor, int(watermark) - OVERLAP_YEARS) if watermark else floor
    current_year = datetime.now(timezone.utc).year

    for year in range(start_year, current_year + 1):
        if force_month:
            _fetch_year_by_month(node_id, mnemonic, year)
        else:
            try:
                rows = _get_rows(_range_url(mnemonic, f"{year}0101", f"{year}1231"))
                if rows:
                    save_raw_ndjson(rows, node_id, fragment=str(year))  # write raw FIRST
            except _TooLarge:
                _fetch_year_by_month(node_id, mnemonic, year)
        save_state(node_id, {"schema_version": STATE_VERSION, "watermark": year})


def _fetch_exchange_site(node_id: str) -> None:
    """Official FX rates, one year per request; incremental by year."""
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    watermark = state.get("watermark")  # last year processed (int)
    start_year = (
        max(FX_FLOOR_YEAR, int(watermark) - OVERLAP_YEARS) if watermark else FX_FLOOR_YEAR
    )
    current_year = datetime.now(timezone.utc).year

    for year in range(start_year, current_year + 1):
        rows = _get_rows(f"{EXCHANGE_SITE}?start={year}0101&end={year}1231&json")
        if rows:
            save_raw_ndjson(rows, node_id, fragment=str(year))  # write raw FIRST
        save_state(node_id, {"schema_version": STATE_VERSION, "watermark": year})


def fetch_one(node_id: str) -> None:
    """Single entry point for every download node. Recovers the dataset from the
    spec id and dispatches to the right strategy."""
    entity = SPEC_ENTITY[node_id]
    if entity == "official-exchange-rates":
        _fetch_exchange_site(node_id)
        return
    mnemonic = MNEMONIC.get(entity, entity)
    if entity in FORCE_MONTH:
        _fetch_windowed(node_id, mnemonic, force_month=True)
        return
    try:
        _fetch_full(node_id, mnemonic)
    except _TooLarge:
        _fetch_windowed(node_id, mnemonic, force_month=False)


# --------------------------------------------------------------------------- #
# Specs — one per entity-union id
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
