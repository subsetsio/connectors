from __future__ import annotations

from subsets_utils import NodeSpec, get, save_raw_ndjson


PREFIX = "u-s-department-of-the-treasury-"
BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
PAGE_SIZE = 5000


ENTITY_ENDPOINTS = {
    "average-interest-rates-treasury-securities-average-interest-rates-on-u-s-treasury-securities": "v2/accounting/od/avg_interest_rates",
    "daily-treasury-statement-operating-cash-balance": "v1/accounting/dts/operating_cash_balance",
    "debt-to-the-penny-debt-to-the-penny": "v2/accounting/od/debt_to_penny",
    "historical-debt-outstanding-historical-debt-outstanding": "v2/accounting/od/debt_outstanding",
    "interest-expense-debt-outstanding-interest-expense-on-the-public-debt-outstanding": "v2/accounting/od/interest_expense",
    "monthly-statement-public-debt-summary-of-treasury-securities-outstanding": "v1/debt/mspd/mspd_table_1",
    "monthly-treasury-statement-summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government": "v1/accounting/mts/mts_table_5",
    "treasury-reporting-rates-exchange-treasury-reporting-rates-of-exchange": "v1/accounting/od/rates_of_exchange",
    "treasury-securities-auctions-data-treasury-securities-auctions-data": "v1/accounting/od/auctions_query",
}


def fetch_table(asset_id: str) -> None:
    entity_id = asset_id.removeprefix(PREFIX)
    endpoint = ENTITY_ENDPOINTS[entity_id]
    url = f"{BASE_URL}/{endpoint}"
    rows = []
    page = 1

    while True:
        response = get(
            url,
            params={"format": "json", "page[size]": PAGE_SIZE, "page[number]": page},
            timeout=(10.0, 120.0),
        )
        response.raise_for_status()
        payload = response.json()
        batch = payload.get("data") or []
        rows.extend(batch)

        meta = payload.get("meta") or {}
        total_pages = int(meta.get("total-pages") or page)
        if page >= total_pages or not batch:
            break
        page += 1

    save_raw_ndjson(rows, asset_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id}", fn=fetch_table)
    for entity_id in sorted(ENTITY_ENDPOINTS)
]
