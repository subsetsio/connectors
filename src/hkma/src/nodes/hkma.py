"""HKMA Open API connector.

Hong Kong Monetary Authority Open API (https://api.hkma.gov.hk/public, no auth).
Each entity is one statistical endpoint returning a flat JSON table of records
behind a `{header:{success,err_code,err_msg}, result:{datasize, records:[...]}}`
envelope with offset pagination (100 records/page). One download spec per
entity; one passthrough SQL transform publishes each as a Delta table.

Strategy: stateless full re-pull. Each endpoint always returns its complete
history in a handful of pages (most series < 50 pages), so we re-fetch the whole
table every run and overwrite — no watermark, no incremental filter (the API
exposes none). Raw is written as NDJSON because schemas vary across the 95
endpoints and some endpoints are fetched across several `segment` values whose
record shapes differ; NDJSON absorbs that drift and the transform re-types on read.

A subset of endpoints require a `segment` query param (verified live 2026-06).
For those, every segment is fetched and a `segment` column is added so the
endpoint stays one published table with the segment as a dimension value.

Endpoint paths were re-verified against the live API during implementation; the
legacy data-integrations list had several stale paths (renamed/retired endpoints
and a `fc-resv-assets` -> `fc-resv-assests` typo) which are corrected here.
"""
import time


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE_URL = "https://api.hkma.gov.hk/public"
PAGE_SIZE = 100
MAX_PAGES = 2000  # safety ceiling; HKMA series are short — a hit means runaway

# node_id -> fetch parameters. node_id == f"hkma-{entity_id.lower().replace('_','-')}".
# `path` is relative to BASE_URL; `lang` adds lang=en; `extra` adds fixed query
# params; `segments` (if present) is fetched one value at a time, each tagged
# into a `segment` column.
META = {
    "hkma-asset-quality-ais": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/assetquality-ais"},
    "hkma-asset-quality-retail-banks": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/assetquality-retailbanks"},
    "hkma-balance-sheet-ais": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/balance-sheet-ais"},
    "hkma-balance-sheet-dtc": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/balance-sheet-dtc"},
    "hkma-balance-sheet-lb": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/balance-sheet-lb"},
    "hkma-balance-sheet-rlb": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/balance-sheet-rlb"},
    "hkma-banking-ais-lros": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/number-of-ais-lros"},
    "hkma-capital-adequacy": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/capital-adequacy"},
    "hkma-cmu-outstanding-all-currencies": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/cmu-outstanding-remain-tenor-all-currencies"},
    "hkma-cmu-service": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/cmu-service"},
    "hkma-cmu-turnover-all-currencies": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/cmu-turnover-sec-mkt-remain-tenor-all-currencies"},
    "hkma-composite-interest-rate": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/composite-ir"},
    "hkma-credit-card-lending-survey": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/credit-card-lending-survey"},
    "hkma-currency": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money/currency"},
    "hkma-daily-interbank-liquidity": {"path": "market-data-and-statistics/daily-monetary-statistics/daily-figures-interbank-liquidity"},
    "hkma-daily-monetary-base": {"path": "market-data-and-statistics/daily-monetary-statistics/daily-figures-monetary-base"},
    "hkma-deposits-by-currency": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/customer-deposits-by-currency"},
    "hkma-deposits-by-type-cny": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/customer-deposits-by-type-cny"},
    "hkma-deposits-by-type-hkd-fc": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/customer-deposits-by-type-hkd-fc"},
    "hkma-discount-window-rates-daily": {"path": "market-data-and-statistics/monthly-statistical-bulletin/monetary-operation/disc-win-liquid-adj-win-rates-daily"},
    "hkma-discount-window-rates-endperiod": {"path": "market-data-and-statistics/monthly-statistical-bulletin/monetary-operation/disc-win-liquid-adj-win-rates-endperiod"},
    "hkma-discount-window-rates-periodaverage": {"path": "market-data-and-statistics/monthly-statistical-bulletin/monetary-operation/disc-win-liquid-adj-win-rates-periodaverage"},
    "hkma-economic-statistics": {"path": "market-data-and-statistics/monthly-statistical-bulletin/financial/economic-statistics"},
    "hkma-efbn-closing": {"path": "market-data-and-statistics/daily-monetary-statistics/efbn-closing", "segments": ["Bills", "Notes"]},
    "hkma-efbn-indicative-price": {"path": "market-data-and-statistics/daily-monetary-statistics/efbn-indicative-price", "segments": ["IndicativePrice", "Bills", "Notes"]},
    "hkma-efbn-outstanding-original-maturity": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/efbn-oustanding-original-maturity"},
    "hkma-efbn-outstanding-remaining-tenor": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/efbn-outstanding-remaining-tenor"},
    "hkma-efbn-tender-results-efb": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/efbn-tender-results-efb", "segments": ["28day", "91day", "182day", "364day"]},
    "hkma-efbn-tender-results-efn": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/efbn-tender-results-efn", "segments": ["2year", "3year", "5year", "7year", "10year", "15year"]},
    "hkma-efbn-turnover-original-maturity": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/efbn-turnover-sec-mkt-original-maturity"},
    "hkma-efbn-turnover-remaining-tenor": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/efbn-turnover-sec-mkt-remaining-tenor"},
    "hkma-efbn-yield-daily": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/efbn-yield-daily"},
    "hkma-efbn-yield-endperiod": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/efbn-yield-endperiod"},
    "hkma-efbn-yield-periodaverage": {"path": "market-data-and-statistics/monthly-statistical-bulletin/efbn/efbn-yield-periodaverage"},
    "hkma-elc-position-all": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/elc-pos-v-all"},
    "hkma-elc-position-mainland-china": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/elc-pos-v-mc"},
    "hkma-exchange-fund-position": {"path": "market-data-and-statistics/monthly-statistical-bulletin/ef-fc-resv-assets/ef-bal-sheet-abridged"},
    "hkma-exchange-rates-daily": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-daily"},
    "hkma-exchange-rates-endperiod": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-endperiod"},
    "hkma-exchange-rates-periodaverage": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-periodaverage"},
    "hkma-fc-position-all": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/fc-position-all"},
    "hkma-fc-position-usd": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/fc-position-usd"},
    "hkma-foreign-currency-reserve-assets": {"path": "market-data-and-statistics/monthly-statistical-bulletin/ef-fc-resv-assets/fc-resv-assests"},
    "hkma-govbond-new-issuance": {"path": "market-data-and-statistics/monthly-statistical-bulletin/gov-bond/new-issuance-amt-gov-bonds"},
    "hkma-govbond-outstanding-original-maturity": {"path": "market-data-and-statistics/monthly-statistical-bulletin/gov-bond/out-amt-gov-bonds-original-maturity"},
    "hkma-govbond-outstanding-remaining-tenor": {"path": "market-data-and-statistics/monthly-statistical-bulletin/gov-bond/out-amt-gov-bonds-remaining-tenor"},
    "hkma-govbond-price-yield-daily": {"path": "market-data-and-statistics/monthly-statistical-bulletin/gov-bond/instit-bond-price-yield-daily", "segments": ["Benchmark", "OutstandPrices", "OutstandYields", "MaturedPrices", "MaturedYields"]},
    "hkma-govbond-price-yield-endperiod": {"path": "market-data-and-statistics/monthly-statistical-bulletin/gov-bond/instit-bond-price-yield-endperiod", "segments": ["Benchmark", "OutstandPrices", "OutstandYields", "MaturedPrices", "MaturedYields"]},
    "hkma-govbond-price-yield-periodaverage": {"path": "market-data-and-statistics/monthly-statistical-bulletin/gov-bond/instit-bond-price-yield-periodaverage", "segments": ["Benchmark", "OutstandPrices", "OutstandYields", "MaturedPrices", "MaturedYields"]},
    "hkma-govbond-tender-results": {"path": "market-data-and-statistics/monthly-statistical-bulletin/gov-bond/tender-results-gov-bonds-ibip", "segments": ["2year", "3year", "5year", "10year", "15year"]},
    "hkma-govbond-turnover-original-maturity": {"path": "market-data-and-statistics/monthly-statistical-bulletin/gov-bond/sec-mar-turnover-govbonds-ibip-original-maturity"},
    "hkma-govbond-turnover-remaining-tenor": {"path": "market-data-and-statistics/monthly-statistical-bulletin/gov-bond/sec-mar-turnover-govbonds-ibip-remain-tenor"},
    "hkma-hkd-debt-instruments-new-issues": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money-markets/ni-hkd-debt-inst-oth-efbn"},
    "hkma-hkd-debt-instruments-outstanding": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money-markets/osamt-hkd-debtinst-otherthan-efbn"},
    "hkma-hkd-forward-rates-daily": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/hkd-fer-daily"},
    "hkma-hkd-forward-rates-endperiod": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/hkd-fer-endperiod"},
    "hkma-hkd-forward-rates-periodaverage": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/hkd-fer-periodaverage"},
    "hkma-hkd-interbank-transactions": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money-markets/hkd-interbank-trans"},
    "hkma-hkd-interest-rates-effective": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/hkd-ir-effdates"},
    "hkma-hkd-interest-rates-periodaverage": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/hkd-ir-periodaverage"},
    "hkma-interbank-rates-daily": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/hk-interbank-ir-daily"},
    "hkma-interbank-rates-endperiod": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/hk-interbank-ir-endperiod"},
    "hkma-interbank-rates-periodaverage": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/hk-interbank-ir-periodaverage"},
    "hkma-liabilities-to-other-ais": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money-markets/liab-dt-other-ais"},
    "hkma-liquidity": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/liquidity"},
    "hkma-loans-by-sector-ais": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/loans-by-sector-ais"},
    "hkma-loans-by-sector-dtc": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/loans-by-sector-dtc"},
    "hkma-loans-by-sector-lb": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/loans-by-sector-lb"},
    "hkma-loans-by-sector-rlb": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/loans-by-sector-rlb"},
    "hkma-loans-by-type-ais": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/loans-by-type-ais"},
    "hkma-loans-by-type-dtc": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/loans-by-type-dtc"},
    "hkma-loans-by-type-lb": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/loans-by-type-lb"},
    "hkma-loans-by-type-rlb": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/loans-by-type-rlb"},
    "hkma-mainland-lending": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/mr-lending"},
    "hkma-mainland-lending-ais": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/mr-lending-ais-type"},
    "hkma-mainland-lending-borrowers-type": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/mr-lending-borrowers-type"},
    "hkma-market-operation-daily": {"path": "market-data-and-statistics/monthly-statistical-bulletin/monetary-operation/market-operation-daily"},
    "hkma-market-operation-periodaverage": {"path": "market-data-and-statistics/monthly-statistical-bulletin/monetary-operation/market-operation-periodaverage"},
    "hkma-monetary-base-daily": {"path": "market-data-and-statistics/monthly-statistical-bulletin/monetary-operation/monetary-base-daily"},
    "hkma-monetary-base-endperiod": {"path": "market-data-and-statistics/monthly-statistical-bulletin/monetary-operation/monetary-base-endperiod"},
    "hkma-monetary-statistics": {"path": "market-data-and-statistics/monthly-statistical-bulletin/financial/monetary-statistics"},
    "hkma-money-components-seasonally-adjusted-hkd": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money/components-seasonally-adjusted-hkd"},
    "hkma-money-supply-adjusted": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money/supply-adjusted"},
    "hkma-money-supply-components-all": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money/supply-components-all"},
    "hkma-money-supply-components-fc": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money/supply-components-fc"},
    "hkma-money-supply-components-hkd": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money/supply-components-hkd"},
    "hkma-money-supply-unadjusted-fc": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money/supply-unadjusted-fc"},
    "hkma-ncds-issued-in-hk": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money-markets/ncds-issued-in-hk"},
    "hkma-ncds-turnover-secondary-market": {"path": "market-data-and-statistics/monthly-statistical-bulletin/money-markets/turnover-ncds-sec-mar-hk-ais"},
    "hkma-register-ais-lros": {"path": "bank-svf-info/register-ais-lros", "lang": True},
    "hkma-register-svf-licensees": {"path": "bank-svf-info/register-svf-licensees", "lang": True, "segments": ["SVFLic", "LBIssuingSVF", "LBNotIssuingSVF"]},
    "hkma-renminbi-deposit-rates": {"path": "market-data-and-statistics/monthly-statistical-bulletin/er-ir/renminbi-dr"},
    "hkma-residential-mortgage-negative-equity": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/residential-mortgage-loans-neg-equity"},
    "hkma-residential-mortgage-survey": {"path": "market-data-and-statistics/monthly-statistical-bulletin/banking/residential-mortgage-survey"},
    "hkma-rmb-liquidity-facility-usage": {"path": "market-data-and-statistics/daily-monetary-statistics/usage-rmb-liquidity-fac"},
}


@transient_retry(min_wait=2, max_wait=60)
def _get_page(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_segment(url: str, base_params: dict) -> list:
    """Page through one endpoint (one segment) and return all records."""
    rows = []
    offset = 0
    for _ in range(MAX_PAGES):
        params = dict(base_params, offset=offset)
        data = _get_page(url, params)
        header = data.get("header", {})
        if not header.get("success"):
            # 200-with-error or 4xx surfaced as a clean envelope: a permanent
            # contract problem (bad path / bad param), not transient. Fail loud.
            raise RuntimeError(
                f"HKMA API error for {url} params={params}: "
                f"{header.get('err_code')} {header.get('err_msg')}"
            )
        records = data.get("result", {}).get("records", []) or []
        rows.extend(records)
        if len(records) < PAGE_SIZE:
            return rows
        offset += PAGE_SIZE
        time.sleep(0.1)  # courtesy pause; API documents no rate limit
    raise RuntimeError(
        f"HKMA pagination exceeded {MAX_PAGES} pages for {url} — "
        "endpoint grew unexpectedly or pagination is not terminating"
    )


def fetch_one(node_id: str) -> None:
    """Fetch one HKMA endpoint in full and write it as NDJSON raw.

    Stateless full re-pull: the endpoint returns its entire history each call,
    so we overwrite every run. Segment endpoints are fetched once per segment
    value and tagged with a `segment` column.
    """
    meta = META[node_id]
    url = f"{BASE_URL}/{meta['path']}"
    base_params = {}
    if meta.get("lang"):
        base_params["lang"] = "en"
    if meta.get("extra"):
        base_params.update(meta["extra"])

    segments = meta.get("segments")
    if segments:
        rows = []
        for seg in segments:
            seg_rows = _fetch_segment(url, dict(base_params, segment=seg))
            for r in seg_rows:
                r["segment"] = seg
            rows.extend(seg_rows)
    else:
        rows = _fetch_segment(url, base_params)

    if not rows:
        raise RuntimeError(f"{node_id}: endpoint {url} returned 0 records")

    save_raw_ndjson(rows, node_id)
    print(f"[hkma] {node_id}: {len(rows):,} records")


DOWNLOAD_SPECS = [
    NodeSpec(id=node_id, fn=fetch_one, kind="download")
    for node_id in META
]

# Per-endpoint grain declarations (key = published-table grain, temporal =
# primary observation-period column). Purely declarative lookup keyed by
# download-spec id. Most endpoints are one-observation-per-period series keyed by
# their period column (end_of_month/quarter/date/day). Segment endpoints whose
# grain also spans the segment/instrument dimension are left keyless but keep
# their period column as temporal; the two registers are keyed by identity.
_GRAIN = {
    "hkma-asset-quality-ais": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-asset-quality-retail-banks": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-balance-sheet-ais": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-balance-sheet-dtc": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-balance-sheet-lb": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-balance-sheet-rlb": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-banking-ais-lros": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-capital-adequacy": {"key": ("end_of_quarter",), "temporal": "end_of_quarter"},
    "hkma-cmu-outstanding-all-currencies": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-cmu-service": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-cmu-turnover-all-currencies": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-composite-interest-rate": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-credit-card-lending-survey": {"key": ("end_of_quarter",), "temporal": "end_of_quarter"},
    "hkma-currency": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-daily-interbank-liquidity": {"key": ("end_of_date",), "temporal": "end_of_date"},
    "hkma-daily-monetary-base": {"key": ("end_of_date",), "temporal": "end_of_date"},
    "hkma-deposits-by-currency": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-deposits-by-type-cny": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-deposits-by-type-hkd-fc": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-discount-window-rates-daily": {"key": ("end_of_day",), "temporal": "end_of_day"},
    "hkma-discount-window-rates-endperiod": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-discount-window-rates-periodaverage": {"temporal": "end_of_month"},
    "hkma-efbn-closing": {"temporal": "end_of_date"},
    "hkma-efbn-indicative-price": {"temporal": "end_of_date"},
    "hkma-efbn-outstanding-original-maturity": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-efbn-outstanding-remaining-tenor": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-efbn-tender-results-efb": {"temporal": "issue_date"},
    "hkma-efbn-tender-results-efn": {"temporal": "issue_date"},
    "hkma-efbn-turnover-original-maturity": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-efbn-turnover-remaining-tenor": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-efbn-yield-daily": {"key": ("end_of_day",), "temporal": "end_of_day"},
    "hkma-efbn-yield-endperiod": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-efbn-yield-periodaverage": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-elc-position-all": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-elc-position-mainland-china": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-exchange-fund-position": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-exchange-rates-daily": {"key": ("end_of_day",), "temporal": "end_of_day"},
    "hkma-exchange-rates-endperiod": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-exchange-rates-periodaverage": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-fc-position-all": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-fc-position-usd": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-foreign-currency-reserve-assets": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-govbond-new-issuance": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-govbond-outstanding-original-maturity": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-govbond-outstanding-remaining-tenor": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-govbond-price-yield-daily": {"temporal": "end_of_day"},
    "hkma-govbond-price-yield-endperiod": {"temporal": "end_of_month"},
    "hkma-govbond-price-yield-periodaverage": {"temporal": "end_of_month"},
    "hkma-govbond-tender-results": {"key": ("issue_date",), "temporal": "issue_date"},
    "hkma-govbond-turnover-original-maturity": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-govbond-turnover-remaining-tenor": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-hkd-debt-instruments-new-issues": {"key": ("end_of_quarter",), "temporal": "end_of_quarter"},
    "hkma-hkd-debt-instruments-outstanding": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-hkd-forward-rates-daily": {"key": ("end_of_day",), "temporal": "end_of_day"},
    "hkma-hkd-forward-rates-endperiod": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-hkd-forward-rates-periodaverage": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-hkd-interbank-transactions": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-hkd-interest-rates-effective": {"key": ("effect_date",), "temporal": "effect_date"},
    "hkma-hkd-interest-rates-periodaverage": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-interbank-rates-daily": {"key": ("end_of_day",), "temporal": "end_of_day"},
    "hkma-interbank-rates-endperiod": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-interbank-rates-periodaverage": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-liabilities-to-other-ais": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-liquidity": {"key": ("end_of_quarter",), "temporal": "end_of_quarter"},
    "hkma-loans-by-sector-ais": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-loans-by-sector-dtc": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-loans-by-sector-lb": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-loans-by-sector-rlb": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-loans-by-type-ais": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-loans-by-type-dtc": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-loans-by-type-lb": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-loans-by-type-rlb": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-mainland-lending-ais": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-mainland-lending-borrowers-type": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-mainland-lending": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-market-operation-daily": {"key": ("end_of_day",), "temporal": "end_of_day"},
    "hkma-market-operation-periodaverage": {"temporal": "end_of_month"},
    "hkma-monetary-base-daily": {"key": ("end_of_day",), "temporal": "end_of_day"},
    "hkma-monetary-base-endperiod": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-money-components-seasonally-adjusted-hkd": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-money-supply-adjusted": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-money-supply-components-all": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-money-supply-components-fc": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-money-supply-components-hkd": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-money-supply-unadjusted-fc": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-ncds-issued-in-hk": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-ncds-turnover-secondary-market": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-register-ais-lros": {"key": ("name",)},
    "hkma-register-svf-licensees": {"key": ("licence_no",), "temporal": "effective_date"},
    "hkma-renminbi-deposit-rates": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-residential-mortgage-negative-equity": {"key": ("end_of_quarter",), "temporal": "end_of_quarter"},
    "hkma-residential-mortgage-survey": {"key": ("end_of_month",), "temporal": "end_of_month"},
    "hkma-rmb-liquidity-facility-usage": {"key": ("end_of_date",), "temporal": "end_of_date"},
}

# One passthrough transform per endpoint: the raw NDJSON is already a clean flat
# table, so the transform just republishes it (and acts as the >0-row gate). The
# runtime registers each dep as a view over read_json_auto, which unions the
# record keys — so heterogeneous segment rows surface as columns with nulls.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=f'SELECT * FROM "{spec.id}"',
        **_GRAIN.get(spec.id, {}),
    )
    for spec in DOWNLOAD_SPECS
]
