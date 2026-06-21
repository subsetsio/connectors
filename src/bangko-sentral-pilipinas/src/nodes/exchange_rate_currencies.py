"""BSP daily peso exchange rates vs currencies.

Unlike the Excel statistical workbooks, this dataset comes from the native
'Exchange Rate' SharePoint list as JSON rows (daily peso rates vs ~45
currencies, snapshot). It therefore has its own fetch body (paginated
SharePoint REST), its own parse (per-currency rows), and its own published
schema.

Fetch shape: stateless full re-pull; raw is overwritten each run.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import BASE, _get_json

_EXCH_ID = "bangko-sentral-pilipinas-exchange-rate-currencies"


def fetch_exchange_rate(node_id: str) -> None:
    """Daily peso exchange rates vs currencies — native SharePoint JSON list."""
    asset = node_id
    url = (
        f"{BASE}/_api/web/lists/getByTitle('Exchange%20Rate')/items?$top=5000"
    )
    rows = []
    while url:
        j = _get_json(url)
        for it in j.get("value", []):
            cur = it.get("Title")
            if not cur:
                continue
            rows.append(
                {
                    "currency": cur,
                    "symbol": it.get("Symbol"),
                    "unit": it.get("Unit"),
                    "country_code": it.get("CountryCode"),
                    "group": it.get("Group"),
                    "usd_equivalent": it.get("USDequivalent"),
                    "php_equivalent": it.get("PHPequivalent"),
                    "eur_equivalent": it.get("EURequivalent"),
                    "published_date": it.get("PublishedDate"),
                }
            )
        url = j.get("odata.nextLink")
    if not rows:
        raise AssertionError("exchange-rate: no rows from SharePoint list")
    save_raw_ndjson(rows, asset)


EXCHANGE_RATE_SPECS = [
    NodeSpec(
        id=_EXCH_ID,
        fn=fetch_exchange_rate,
        kind="download",
    ),
]

EXCHANGE_RATE_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_EXCH_ID}-transform",
        deps=[_EXCH_ID],
        sql=f'''
            SELECT
                currency,
                symbol,
                unit,
                country_code,
                "group" AS currency_group,
                TRY_CAST(usd_equivalent AS DOUBLE) AS usd_equivalent,
                TRY_CAST(php_equivalent AS DOUBLE) AS php_equivalent,
                TRY_CAST(eur_equivalent AS DOUBLE) AS eur_equivalent,
                published_date
            FROM "{_EXCH_ID}"
            WHERE currency IS NOT NULL
        ''',
    ),
]
