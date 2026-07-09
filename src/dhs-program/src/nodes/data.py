"""DHS /data indicator observations — the fact table.

The /data endpoint REQUIRES a filter (unfiltered -> HTTP 400), so we crawl it
per-country: enumerate the country codes from /countries, then page each
country's records with perpage=5000. Each country is written as its own NDJSON
batch `dhs-program-data-<cc>`; the transform's view globs `dhs-program-data-*`
and unions them.
"""
from __future__ import annotations

from subsets_utils import NodeSpec, save_raw_ndjson

from utils import BASE, clean, fetch_all

DATA_URL = f"{BASE}/data"
COUNTRIES_URL = f"{BASE}/countries"


def fetch_data(node_id: str) -> None:
    """Crawl the /data fact table per country (the endpoint rejects unfiltered
    requests). Each country is its own NDJSON batch `dhs-program-data-<cc>`."""
    countries = fetch_all(COUNTRIES_URL)
    codes = sorted({c["DHS_CountryCode"] for c in countries if c.get("DHS_CountryCode")})
    if not codes:
        raise RuntimeError("DHS countries endpoint returned no country codes")
    for cc in codes:
        records = fetch_all(DATA_URL, countryIds=cc)
        if not records:
            continue
        save_raw_ndjson((clean(r) for r in records), node_id, fragment=cc.lower())


DOWNLOAD_SPECS = [
    NodeSpec(id="dhs-program-data", fn=fetch_data, kind="download"),
]
