"""Download nodes for the DHS Program public indicator API."""
from __future__ import annotations

from subsets_utils import NodeSpec, save_raw_ndjson

from utils import BASE, clean, fetch_all

COUNTRIES_URL = f"{BASE}/countries"
DATA_URL = f"{BASE}/data"
INDICATORS_URL = f"{BASE}/indicators"
SURVEYS_URL = f"{BASE}/surveys"
TAGS_URL = f"{BASE}/tags"


def fetch_countries(node_id: str) -> None:
    records = fetch_all(COUNTRIES_URL)
    save_raw_ndjson((clean(r) for r in records), node_id)


def fetch_data(node_id: str) -> None:
    countries = fetch_all(COUNTRIES_URL)
    codes = sorted({c["DHS_CountryCode"] for c in countries if c.get("DHS_CountryCode")})
    if not codes:
        raise RuntimeError("DHS countries endpoint returned no country codes")

    for code in codes:
        records = fetch_all(DATA_URL, countryIds=code)
        if records:
            save_raw_ndjson((clean(r) for r in records), node_id, fragment=code.lower())


def fetch_indicators(node_id: str) -> None:
    records = fetch_all(INDICATORS_URL)
    save_raw_ndjson((clean(r) for r in records), node_id)


def fetch_surveys(node_id: str) -> None:
    records = fetch_all(SURVEYS_URL)
    save_raw_ndjson((clean(r) for r in records), node_id)


def fetch_tags(node_id: str) -> None:
    records = fetch_all(TAGS_URL)
    save_raw_ndjson((clean(r) for r in records), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="dhs-program-countries", fn=fetch_countries, kind="download"),
    NodeSpec(id="dhs-program-data", fn=fetch_data, kind="download"),
    NodeSpec(id="dhs-program-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="dhs-program-surveys", fn=fetch_surveys, kind="download"),
    NodeSpec(id="dhs-program-tags", fn=fetch_tags, kind="download"),
]
