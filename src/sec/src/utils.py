"""Shared transport + concept config for the SEC EDGAR connector.

Holds the XBRL Frames API client (rate-limited, retried), the period
enumeration helpers, and the curated concept set used by both the concepts
catalog and the facts long-table. No NodeSpec definitions live here.

A descriptive User-Agent header is mandatory or SEC returns 403; www.sec.gov is
stricter than data.sec.gov, so each fetch fn sets it via configure_http.
SEC fair-access limit is 10 requests/second.
"""
import datetime

import httpx
from ratelimit import limits, sleep_and_retry

from subsets_utils import get, transient_retry

# ASCII-only — non-ASCII in a header value raises UnicodeEncodeError.
USER_AGENT = "subsets.io connector nathan@subsets.io"

# SEC XBRL financial-reporting mandate began in 2009; nothing earlier exists.
XBRL_START_YEAR = 2009

# Curated set of widely-reported XBRL concepts spanning the income statement,
# balance sheet, and cash-flow statement, plus one dei share-count concept.
# Each: (taxonomy, tag, unit, concept_type). "duration" concepts report over a
# period (annual CY####, quarterly CY####Q#); "instant" concepts are point-in-
# time balances (CY####Q#I).
CONCEPTS = [
    ("us-gaap", "Revenues", "USD", "duration"),
    ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax", "USD", "duration"),
    ("us-gaap", "CostOfRevenue", "USD", "duration"),
    ("us-gaap", "GrossProfit", "USD", "duration"),
    ("us-gaap", "OperatingIncomeLoss", "USD", "duration"),
    ("us-gaap", "NetIncomeLoss", "USD", "duration"),
    ("us-gaap", "ResearchAndDevelopmentExpense", "USD", "duration"),
    ("us-gaap", "EarningsPerShareBasic", "USD-per-shares", "duration"),
    ("us-gaap", "EarningsPerShareDiluted", "USD-per-shares", "duration"),
    ("us-gaap", "NetCashProvidedByUsedInOperatingActivities", "USD", "duration"),
    ("us-gaap", "NetCashProvidedByUsedInInvestingActivities", "USD", "duration"),
    ("us-gaap", "NetCashProvidedByUsedInFinancingActivities", "USD", "duration"),
    ("us-gaap", "PaymentsToAcquirePropertyPlantAndEquipment", "USD", "duration"),
    ("us-gaap", "Assets", "USD", "instant"),
    ("us-gaap", "AssetsCurrent", "USD", "instant"),
    ("us-gaap", "Liabilities", "USD", "instant"),
    ("us-gaap", "LiabilitiesCurrent", "USD", "instant"),
    ("us-gaap", "StockholdersEquity", "USD", "instant"),
    ("us-gaap", "CashAndCashEquivalentsAtCarryingValue", "USD", "instant"),
    ("us-gaap", "InventoryNet", "USD", "instant"),
    ("us-gaap", "RetainedEarningsAccumulatedDeficit", "USD", "instant"),
    ("us-gaap", "LongTermDebtNoncurrent", "USD", "instant"),
    ("dei", "EntityCommonStockSharesOutstanding", "shares", "instant"),
]


# --- transport ------------------------------------------------------------


@transient_retry(min_wait=2, max_wait=60)
@sleep_and_retry
@limits(calls=7, period=1)  # SEC fair-access is 10 req/s; stay under it
def fetch_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def frame_url(taxonomy: str, tag: str, unit: str, period: str) -> str:
    return (
        f"https://data.sec.gov/api/xbrl/frames/"
        f"{taxonomy}/{tag}/{unit}/{period}.json"
    )


def try_frame(taxonomy: str, tag: str, unit: str, period: str):
    """Fetch one Frames response; return the parsed dict, or None when the
    source has no data for this concept/period (404) or rejects it (other 4xx).
    Transient errors are retried inside fetch_json; bugs propagate."""
    url = frame_url(taxonomy, tag, unit, period)
    try:
        return fetch_json(url)
    except httpx.HTTPStatusError as exc:
        code = exc.response.status_code
        if code == 404:
            return None  # no data for this period — expected and common
        if 400 <= code < 500:
            print(f"  permanent {code} on {url}; skipping")
            return None
        raise


def years():
    # End year discovered at runtime; 404s bound where data actually exists.
    now_year = datetime.datetime.now(datetime.timezone.utc).year
    return range(XBRL_START_YEAR, now_year + 1)


def periods_for(concept_type: str) -> list[str]:
    out = []
    for y in years():
        if concept_type == "duration":
            out.append(f"CY{y}")
            for q in (1, 2, 3, 4):
                out.append(f"CY{y}Q{q}")
        else:  # instant
            for q in (1, 2, 3, 4):
                out.append(f"CY{y}Q{q}I")
    return out
