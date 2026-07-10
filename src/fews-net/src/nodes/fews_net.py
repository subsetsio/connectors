"""FEWS NET (FDW) connector.

Publishes four public time-series domains from the FEWS NET Data Warehouse
REST API (https://fdw.fews.net/api), one Delta table each:

  - ipcphase               IPC acute food insecurity phase classifications
  - ipcpopulationsize      food-insecure population estimates
  - marketpricefacts       staple market prices
  - tradeflowquantityvalue cross-border trade flows

Fetch strategy — stateless full re-pull each run (raw is run-scoped, so a run
always starts clean and a re-pull picks up upstream revisions for free). Each
domain is streamed row-by-row to a single `ndjson.gz` raw asset so memory stays
bounded regardless of corpus size (market prices is ~4.1M rows). Pagination is
offset-based and re-sends the full param set (incl. `fields`) on every page, so
the column projection stays identical across pages.

`ipcphase` is fetched per-country: the unfiltered query is pathologically slow
(~100s even for a single row, due to a heavy server-side join), but a
`country_code` filter scopes it to sub-second. The other three page globally.
The CSV extract format is broken server-side (pandas import error), so we use
JSON only — see research.
"""

import json

from subsets_utils import NodeSpec, get, raw_writer, transient_retry

BASE = "https://fdw.fews.net/api"
PAGE_SIZE = 100000  # server caps the real page below this; we follow it via offset

# Minimal column projection for the 4.1M-row price table — drops the expensive
# computed pct_change/N-year-average columns that roughly double per-page latency.
MARKET_FIELDS = (
    "id,country,admin_1,admin_2,market,cpcv2,product,price_type,product_source,"
    "period_date,start_date,value,currency,unit,common_unit,common_currency,"
    "common_unit_price,common_currency_price"
)

# domain (== entity id) -> fetch config
DOMAINS = {
    "ipcphase": {"endpoint": "ipcphase", "fields": "simple", "per_country": True},
    "ipcpopulationsize": {"endpoint": "ipcpopulationsize", "fields": "simple", "per_country": False},
    "marketpricefacts": {"endpoint": "marketpricefacts", "fields": MARKET_FIELDS, "per_country": False},
    "tradeflowquantityvalue": {"endpoint": "tradeflowquantityvalue", "fields": "simple", "per_country": False},
}


@transient_retry()
def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.json()


def _country_codes() -> list[str]:
    """ISO 3166-1 alpha-2 codes from the FDW /country/ reference endpoint."""
    data = _get_json(f"{BASE}/country/", {"format": "json", "page_size": 1000})
    rows = data.get("results") if isinstance(data, dict) else data
    return [r["iso3166a2"] for r in (rows or []) if r.get("iso3166a2")]


def _iter_pages(endpoint: str, fields: str, extra: dict | None = None):
    """Yield rows from one datapoint endpoint via offset pagination.

    Re-sends every param (incl. `fields`) on each request so the projection is
    stable across pages. Terminates on an empty page or once offset reaches the
    server-reported count, whichever comes first.
    """
    url = f"{BASE}/{endpoint}/"
    base = {"format": "json", "fields": fields, "page_size": PAGE_SIZE}
    if extra:
        base.update(extra)
    offset = 0
    while True:
        data = _get_json(url, {**base, "offset": offset})
        rows = data.get("results") or []
        if not rows:
            return
        yield from rows
        offset += len(rows)
        count = data.get("count")
        if count is not None and offset >= count:
            return


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    domain = node_id[len("fews-net-"):]
    cfg = DOMAINS[domain]
    n = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
        if cfg["per_country"]:
            for cc in _country_codes():
                for row in _iter_pages(cfg["endpoint"], cfg["fields"], {"country_code": cc}):
                    f.write(json.dumps(row, separators=(",", ":")))
                    f.write("\n")
                    n += 1
        else:
            for row in _iter_pages(cfg["endpoint"], cfg["fields"]):
                f.write(json.dumps(row, separators=(",", ":")))
                f.write("\n")
                n += 1
    if n == 0:
        raise RuntimeError(f"{asset}: fetched 0 rows")
    print(f"  {asset}: wrote {n:,} rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="fews-net-ipcphase", fn=fetch_one, kind="download"),
    NodeSpec(id="fews-net-ipcpopulationsize", fn=fetch_one, kind="download"),
    NodeSpec(id="fews-net-marketpricefacts", fn=fetch_one, kind="download"),
    NodeSpec(id="fews-net-tradeflowquantityvalue", fn=fetch_one, kind="download"),
]
