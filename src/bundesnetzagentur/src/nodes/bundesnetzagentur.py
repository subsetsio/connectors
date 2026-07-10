"""Bundesnetzagentur — SMARD electricity market data connector.

Mechanism: smard_rest (https://www.smard.de/app/chart_data). For each
(module, region) time series we GET index_day.json to list yearly chunk
timestamps, then GET each chunk and concatenate its `series` ([ms, value]
pairs). We use the **daily** resolution: each series is ~12 yearly chunks
(vs ~600 weekly chunks at hourly), so the whole corpus is a few-thousand
small requests — cheap enough for a stateless full re-pull every run, which
also picks up SMARD's revisions of recent days for free. Daily values are the
aggregate of the hourly data (MWh/day for the MW feeds; EUR/MWh daily mean for
prices). No auth, no rate limit (CDN-served static JSON). CC BY 4.0.

Four feeds, each a distinct published subset (different schema):
  generation_actual    realized generation by source, region = DE + 4 TSO zones
  consumption          grid/residual/pumped-storage load, same regions
  generation_forecast  day-ahead forecast generation by source, same regions
  prices_dayahead      day-ahead wholesale price per bidding zone (region DE-LU)
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://www.smard.de/app/chart_data"
RESOLUTION = "day"

# ---- module (filter) -> English label, per SMARD's documented filter enum ----

GENERATION = {
    "1223": "Lignite",
    "1224": "Nuclear",
    "1225": "Wind offshore",
    "1226": "Hydropower",
    "1227": "Other conventional",
    "1228": "Other renewable",
    "4066": "Biomass",
    "4067": "Wind onshore",
    "4068": "Solar PV",
    "4069": "Hard coal",
    "4070": "Pumped storage",
    "4071": "Natural gas",
}

CONSUMPTION = {
    "410": "Total grid load",
    "4359": "Residual load",
    "4387": "Pumped storage consumption",
}

FORECAST = {
    "122": "Total",
    "123": "Wind onshore",
    "125": "Solar PV",
    "715": "Other",
    "5097": "Wind and solar",
    "3791": "Wind offshore",
}

# Day-ahead wholesale prices: the module id IS the bidding zone; all queried
# under region DE-LU (the market-price comparison view). Labels per the
# documented enum; module 258 omitted (documented as a duplicate of 257).
PRICES = {
    "4169": "Germany/Luxembourg",
    "5078": "Neighbours DE/LU",
    "4170": "Austria",
    "4996": "Belgium",
    "4997": "Norway 2",
    "252": "Denmark 1",
    "253": "Denmark 2",
    "254": "France",
    "255": "Italy (North)",
    "256": "Netherlands",
    "257": "Poland",
    "259": "Switzerland",
    "260": "Slovenia",
    "261": "Czech Republic",
    "262": "Hungary",
}

TSO_REGIONS = ["DE", "50Hertz", "Amprion", "TenneT", "TransnetBW"]

RAW_SCHEMA = pa.schema([
    ("date_ms", pa.int64()),
    ("region", pa.string()),
    ("series_code", pa.string()),
    ("series_label", pa.string()),
    ("value", pa.float64()),
])

# --------------------------------------------------------------------------
# HTTP with honest retry classification


@transient_retry(min_wait=2, max_wait=60)
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None  # combination does not exist — caller skips
    resp.raise_for_status()
    return resp.json()


def _index(module: str, region: str):
    data = _get_json(f"{BASE}/{module}/{region}/index_{RESOLUTION}.json")
    if not data:
        return []
    return data.get("timestamps", [])


def _chunk(module: str, region: str, ts: int):
    data = _get_json(
        f"{BASE}/{module}/{region}/{module}_{region}_{RESOLUTION}_{ts}.json"
    )
    if not data:
        return []
    return data.get("series", [])


def _fetch_feed(asset: str, modules: dict, regions: list) -> None:
    rows = []
    for code, label in modules.items():
        for region in regions:
            for ts in _index(code, region):
                for point in _chunk(code, region, ts):
                    value = point[1]
                    if value is None:
                        continue
                    rows.append({
                        "date_ms": int(point[0]),
                        "region": region,
                        "series_code": code,
                        "series_label": label,
                        "value": float(value),
                    })
    table = pa.Table.from_pylist(rows, schema=RAW_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------
# Per-feed download fns (the runtime passes the spec id == asset name)

def fetch_generation_actual(node_id: str) -> None:
    _fetch_feed(node_id, GENERATION, TSO_REGIONS)


def fetch_consumption(node_id: str) -> None:
    _fetch_feed(node_id, CONSUMPTION, TSO_REGIONS)


def fetch_generation_forecast(node_id: str) -> None:
    _fetch_feed(node_id, FORECAST, TSO_REGIONS)


def fetch_prices_dayahead(node_id: str) -> None:
    _fetch_feed(node_id, PRICES, ["DE-LU"])


DOWNLOAD_SPECS = [
    NodeSpec(id="bundesnetzagentur-generation-actual",
             fn=fetch_generation_actual, kind="download"),
    NodeSpec(id="bundesnetzagentur-consumption",
             fn=fetch_consumption, kind="download"),
    NodeSpec(id="bundesnetzagentur-generation-forecast",
             fn=fetch_generation_forecast, kind="download"),
    NodeSpec(id="bundesnetzagentur-prices-dayahead",
             fn=fetch_prices_dayahead, kind="download"),
]
