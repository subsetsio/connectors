"""NY Fed Markets API downloads — one DOWNLOAD_SPEC per accepted collect entity.

Single unauthenticated REST mechanism (https://markets.newyorkfed.org/api, no
auth, JSON). Each of the 11 asset families returns a table with its own column
list, so each is its own download node. Two endpoint shapes are used, both via
`utils`:

  * date-range search ('.../search.json?startDate=&endDate=') paged in <=89-day
    windows (an undocumented per-request range cap; the legacy connector chunked
    the same way) — reference rates, and the operations families (repo, ambs,
    treasury, seclending, fxs).
  * direct snapshot / listing endpoints (SOMA summary + security-level holdings,
    primary-dealer series catalog + full-history values).

Stateless full re-pull: the whole corpus is modest (low hundreds of MB) and the
search endpoints return revisions in place, so every run re-fetches in full and
overwrites — no watermarks. Transforms are NOT declared here; they are compiled
from the settled model into src/transforms/.
"""

from datetime import date

from subsets_utils import NodeSpec, get, save_raw_ndjson, transient_retry
from utils import BASE, flatten_operations, get_json, project, search


# --------------------------------------------------------------------------- #
# Reference rates
# --------------------------------------------------------------------------- #

_RATE_FIELDS = (
    "effectiveDate", "type", "percentRate",
    "percentPercentile1", "percentPercentile25",
    "percentPercentile75", "percentPercentile99",
    "volumeInBillions", "targetRateFrom", "targetRateTo",
    "average30day", "average90day", "average180day", "index",
    "revisionIndicator",
)


def fetch_reference_rates_unsecured(node_id: str) -> None:
    rows = [
        project(r, _RATE_FIELDS)
        for r in search("rates/all/search.json?startDate={startDate}&endDate={endDate}",
                        "refRates", start=date(2016, 3, 1))
        if r.get("type") in ("EFFR", "OBFR")
    ]
    save_raw_ndjson(rows, node_id)


def fetch_reference_rates_secured(node_id: str) -> None:
    rows = [
        project(r, _RATE_FIELDS)
        for r in search("rates/secured/all/search.json?startDate={startDate}&endDate={endDate}",
                        "refRates", start=date(2018, 4, 2))
        if r.get("type") in ("SOFR", "BGCR", "TGCR", "SOFRAI")
    ]
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# SOMA — aggregate summary + security-level holdings
# --------------------------------------------------------------------------- #

_SUMMARY_FIELDS = (
    "asOfDate", "bills", "notesbonds", "tips", "frn",
    "tipsInflationCompensation", "mbs", "cmbs", "agencies", "total",
)

_HOLDING_FIELDS = (
    "asOfDate", "cusip", "securityType", "maturityDate", "issuer",
    "coupon", "spread", "parValue", "inflationCompensation",
    "percentOutstanding", "changeFromPriorWeek", "changeFromPriorYear",
)


def fetch_soma_summary(node_id: str) -> None:
    payload = get_json("soma/summary.json")
    summary = payload.get("soma", {}).get("summary", [])
    rows = [project(r, _SUMMARY_FIELDS) for r in summary]
    save_raw_ndjson(rows, node_id)


def fetch_soma_holdings(node_id: str) -> None:
    # Latest as-of snapshot (security-level). The summary lists every as-of date.
    payload = get_json("soma/summary.json")
    summary = payload.get("soma", {}).get("summary", [])
    as_of = max(s["asOfDate"] for s in summary if s.get("asOfDate"))
    rows = []
    for group, path in (
        ("Treasury", f"soma/tsy/get/all/asof/{as_of}.json"),
        ("Agency", f"soma/agency/get/asof/{as_of}.json"),
    ):
        holdings = get_json(path).get("soma", {}).get("holdings", [])
        rows.extend(
            project(h, _HOLDING_FIELDS, extra={"instrumentGroup": group})
            for h in holdings
        )
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# Temporary open-market operations (parent op + flattened per-detail rows)
# --------------------------------------------------------------------------- #

_REPO_PARENT = (
    "operationId", "operationDate", "operationType", "operationMethod",
    "settlementDate", "maturityDate", "term", "termCalenderDays",
    "settlementType", "totalAmtSubmitted", "totalAmtAccepted",
)
_REPO_DETAIL = (
    "securityType", "amtSubmitted", "amtAccepted",
    "percentOfferingRate", "percentAwardRate", "percentWeightedAverageRate",
)

_AMBS_PARENT = (
    "operationId", "operationDate", "operationType", "operationDirection",
    "method", "classType", "settlementDate",
    "totalAmtSubmittedPar", "totalAmtAcceptedPar",
)
_AMBS_DETAIL = ("securityDescription", "amtAcceptedPar", "inclusionExclusionFlag")

_TSY_PARENT = (
    "operationId", "operationDate", "operationType", "operationDirection",
    "settlementDate", "maturityRangeStart", "maturityRangeEnd",
    "auctionMethod", "totalParAmtSubmitted", "totalParAmtAccepted",
)
_TSY_DETAIL = (
    "cusip", "securityDescription", "parAmountAccepted",
    "weightedAvgAccptPrice", "leastFavoriteAccptPrice",
)

_SECLEND_PARENT = (
    "operationId", "operationDate", "operationType",
    "settlementDate", "maturityDate",
)
_SECLEND_DETAIL = (
    "cusip", "securityDescription", "parAmtSubmitted", "parAmtAccepted",
    "weightedAverageRate", "somaHoldings", "theoAvailToBorrow",
    "actualAvailToBorrow", "outstandingLoans",
)


def fetch_repo_operations(node_id: str) -> None:
    ops = search("rp/results/search.json?startDate={startDate}&endDate={endDate}",
                 "repo", "operations", start=date(2013, 1, 1))
    save_raw_ndjson(list(flatten_operations(ops, _REPO_PARENT, _REPO_DETAIL)), node_id)


def fetch_ambs_operations(node_id: str) -> None:
    ops = search("ambs/all/results/details/search.json?startDate={startDate}&endDate={endDate}",
                 "ambs", "auctions", start=date(2013, 1, 1))
    save_raw_ndjson(list(flatten_operations(ops, _AMBS_PARENT, _AMBS_DETAIL)), node_id)


def fetch_treasury_operations(node_id: str) -> None:
    ops = search("tsy/all/results/details/search.json?startDate={startDate}&endDate={endDate}",
                 "treasury", "auctions", start=date(2009, 1, 1))
    save_raw_ndjson(list(flatten_operations(ops, _TSY_PARENT, _TSY_DETAIL)), node_id)


def fetch_securities_lending(node_id: str) -> None:
    ops = search("seclending/all/results/details/search.json?startDate={startDate}&endDate={endDate}",
                 "seclending", "operations", start=date(2008, 1, 1))
    save_raw_ndjson(list(flatten_operations(ops, _SECLEND_PARENT, _SECLEND_DETAIL)), node_id)


# --------------------------------------------------------------------------- #
# FX / central bank liquidity swaps
# --------------------------------------------------------------------------- #

_FXS_FIELDS = (
    "tradeDate", "settlementDate", "maturityDate", "operationType",
    "counterparty", "currency", "termInDays", "amount", "interestRate",
    "isSmallValue", "lastUpdated",
)


def fetch_fx_swaps(node_id: str) -> None:
    rows = [
        project(r, _FXS_FIELDS)
        for r in search("fxs/all/search.json?startDate={startDate}&endDate={endDate}",
                        "fxSwaps", "operations", start=date(2020, 1, 1))
    ]
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------- #
# Primary dealer statistics — series catalog (reference) + long-format values
# --------------------------------------------------------------------------- #

_PD_SERIES_FIELDS = ("seriesbreak", "keyid", "description")


def fetch_primary_dealer_series(node_id: str) -> None:
    listing = get_json("pd/list/timeseries.json").get("pd", {}).get("timeseries", [])
    rows = [project(s, _PD_SERIES_FIELDS) for s in listing if s.get("keyid")]
    save_raw_ndjson(rows, node_id)


@transient_retry()
def _get_pd_series(keyid: str):
    resp = get(f"{BASE}/pd/get/{keyid}.json", timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None  # permanent: series id no longer served, skip it
    resp.raise_for_status()
    return resp.json().get("pd", {}).get("timeseries", [])


def _pd_value_rows():
    listing = get_json("pd/list/timeseries.json").get("pd", {}).get("timeseries", [])
    meta = {}
    for s in listing:
        kid = s.get("keyid")
        if kid and kid not in meta:
            meta[kid] = {"seriesbreak": s.get("seriesbreak"),
                         "description": s.get("description")}
    for keyid, info in meta.items():
        series = _get_pd_series(keyid)
        if not series:
            continue
        for obs in series:
            yield {
                "asofdate": obs.get("asofdate"),
                "keyid": obs.get("keyid") or keyid,
                "value": obs.get("value"),
                "seriesbreak": info["seriesbreak"],
                "description": info["description"],
            }


def fetch_primary_dealer_values(node_id: str) -> None:
    # Generator keeps memory bounded across ~1500 series.
    save_raw_ndjson(_pd_value_rows(), node_id)


# --------------------------------------------------------------------------- #
# Specs — one per accepted collect entity (the entity union)
# --------------------------------------------------------------------------- #

DOWNLOAD_SPECS = [
    NodeSpec(id="ny-fed-reference-rates-unsecured", fn=fetch_reference_rates_unsecured, kind="download"),
    NodeSpec(id="ny-fed-reference-rates-secured", fn=fetch_reference_rates_secured, kind="download"),
    NodeSpec(id="ny-fed-soma-summary", fn=fetch_soma_summary, kind="download"),
    NodeSpec(id="ny-fed-soma-holdings", fn=fetch_soma_holdings, kind="download"),
    NodeSpec(id="ny-fed-repo-operations", fn=fetch_repo_operations, kind="download"),
    NodeSpec(id="ny-fed-ambs-operations", fn=fetch_ambs_operations, kind="download"),
    NodeSpec(id="ny-fed-treasury-operations", fn=fetch_treasury_operations, kind="download"),
    NodeSpec(id="ny-fed-securities-lending", fn=fetch_securities_lending, kind="download"),
    NodeSpec(id="ny-fed-fx-swaps", fn=fetch_fx_swaps, kind="download"),
    NodeSpec(id="ny-fed-primary-dealer-series", fn=fetch_primary_dealer_series, kind="download"),
    NodeSpec(id="ny-fed-primary-dealer-values", fn=fetch_primary_dealer_values, kind="download"),
]
