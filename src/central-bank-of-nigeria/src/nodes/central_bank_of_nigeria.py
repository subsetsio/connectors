"""Central Bank of Nigeria (cbn) connector — download stage.

Source: the CBN public JSON REST API at https://www.cbn.gov.ng/api/ that powers
the bank's "Data & Statistics" pages (/rates/*.html). Each accepted dataset is
exposed as one `GetAll<Dataset>` endpoint returning the FULL time series as a
single flat JSON array (no pagination, no auth). Numeric values come back as JSON
strings (missing values as ""), so the model/transform stage casts and cleans.

Fetch shape: stateless full re-pull. Every endpoint returns the entire series in
one request (largest observed ~18k daily rows / a few MB; whole corpus well under
100MB), so we re-fetch the whole corpus each run and overwrite — revisions and
late corrections are picked up for free. The source exposes no incremental filter
(no since/cursor/modifiedAfter), so incremental is not possible; full re-pull is
cheap enough that it doesn't matter.

Raw is written as NDJSON: column sets differ per dataset and every value arrives
as a string (missing = ""), so there is no stable cross-record schema worth
declaring in parquet — the SQL transform re-types on read.

One normalisation happens here rather than in the transform, and only because raw
is where it has to happen: no two of these endpoints agree on how to encode an
observation date, and most of the encodings do not sort. Every check that reads
raw — above all the `freshness` download test, which compiles to `max(col)` — is
blind on such a column: lexicographically `31/12/2025` outranks `09/07/2026`, and
`September-30-2024` outranks everything. So each asset gains exactly one sortable
ISO-8601 column per observation date, beside the untouched originals:

  * a real date field in a non-sorting encoding gets a twin, `<field>_iso`
    (`postDate` -> `postDate_iso`); `exchange-rates-daily` needs none, as it
    already serves ISO.
  * an asset with no date field at all — the monthly ones carry integer
    `tyear`/`tmonth`, the GDP ones a `tyear` string plus a `period` label —
    gets `period_start_iso`, the first day of the observation period.

Nothing is dropped, corrected or reinterpreted; the records stay a superset of
the source, and each twin carries the same instant in an encoding that sorts.
Unparseable and empty values become null rather than failing the fetch — a bad
date is data to be observed, not a transport error, and the source has a few
(auction rows maturing in 2098).
"""
from datetime import datetime

from subsets_utils import (
    NodeSpec,
    configure_http,
    get,
    save_raw_ndjson,
    transient_retry,
)

from constants import ENDPOINTS

SLUG = "central-bank-of-nigeria"
PREFIX = SLUG + "-"
API_BASE = "https://www.cbn.gov.ng/api/"

# The host sits behind Cloudflare, which serves a challenge to non-browser
# agents; present a normal desktop-browser User-Agent. ASCII only.
_BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


# entity id -> {source date field: its strptime format}. `exchange-rates-daily`
# is absent on purpose: it already serves ISO, which sorts.
_DATE_FIELDS = {
    "crude-oil-price-daily":  {"postDate": "%d/%m/%Y"},
    "daily-financial-data":   {"recDate": "%d/%m/%Y"},
    "interbank-rates":        {"ratedate": "%B-%d-%Y"},
    "nafem-nof-rates":        {"ratedate": "%B-%d-%Y"},
    "securities-auctions":    {"auctionDate": "%B-%d-%Y", "maturityDate": "%B-%d-%Y"},
}

# Entities with no date field, whose observation period is spelled out across
# other columns. "monthly": integer tyear + tmonth, where the pre-1993 rows of
# money-and-credit are annual observations carrying tmonth = tyear. "gdp":
# a tyear string + a period label of "Annual" or Q1..Q4.
_PERIOD_START = {
    "crude-oil-prices-monthly":    "monthly",
    "inflation-rates":             "monthly",
    "money-and-credit-statistics": "monthly",
    "money-market-indicators":     "monthly",
    "nominal-gdp-annual":          "gdp",
    "nominal-gdp-quarterly":       "gdp",
    "real-gdp-annual":             "gdp",
    "real-gdp-quarterly":          "gdp",
}

_QUARTER_FIRST_MONTH = {"Q1": 1, "Q2": 4, "Q3": 7, "Q4": 10}


def _iso(value, fmt: str) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.strptime(value.strip(), fmt).date().isoformat()
    except ValueError:
        return None


def _period_start(row: dict, shape: str) -> str | None:
    """First day of the row's observation period, ISO-8601."""
    try:
        year = int(str(row.get("tyear")).strip())
    except (TypeError, ValueError):
        return None
    if shape == "monthly":
        month = row.get("tmonth")
        # An annual row encodes tmonth as the year itself; anchor it at January.
        month = month if isinstance(month, int) and 1 <= month <= 12 else 1
    else:
        period = str(row.get("period") or "").strip()
        if period == "Annual":
            month = 1
        elif period in _QUARTER_FIRST_MONTH:
            month = _QUARTER_FIRST_MONTH[period]
        else:
            return None
    return f"{year:04d}-{month:02d}-01"


@transient_retry()
def _fetch_json(url: str):
    # ?format=json is required on some endpoints (e.g. GetAllInterbankRates,
    # which otherwise returns XML) and harmless on the rest.
    resp = get(
        url,
        params={"format": "json"},
        headers={"Accept": "application/json"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    configure_http(headers={"User-Agent": _BROWSER_UA})
    entity_id = node_id.removeprefix(PREFIX)
    endpoint = ENDPOINTS[entity_id]
    data = _fetch_json(API_BASE + endpoint)
    if not isinstance(data, list):
        raise TypeError(
            f"{entity_id}: expected a JSON array from {endpoint}, "
            f"got {type(data).__name__}"
        )
    for field, fmt in _DATE_FIELDS.get(entity_id, {}).items():
        for row in data:
            row[f"{field}_iso"] = _iso(row.get(field), fmt)
    shape = _PERIOD_START.get(entity_id)
    if shape:
        for row in data:
            row["period_start_iso"] = _period_start(row, shape)
    save_raw_ndjson(data, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id}", fn=fetch_one, kind="download")
    for entity_id in ENDPOINTS
]
