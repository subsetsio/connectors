"""OCHA connector — HDX HAPI v2 (Humanitarian API, OCHA Centre for Humanitarian Data).

Each entity is one HAPI v2 thematic endpoint delivering a harmonized humanitarian
indicator table with global coverage, subnational (admin0/1/2) breakdowns and a
reference_period time dimension. The country/admin dimensions are columns, not
separate tables.

Fetch shape: stateless full re-pull (shape 1). Every refresh pages the whole
endpoint via offset/limit and overwrites the raw NDJSON. HAPI exposes no
changed-since cursor (only value filters), and the per-endpoint corpora are
modest, so a full re-pull each run is correct and picks up upstream revisions
for free. Raw is NDJSON because the 25 endpoints (13 thematic + 12 metadata/
lookup reference tables) have heterogeneous schemas and one generic fetch fn
serves all of them; the transform re-types on read.

Auth: every request needs an app_identifier. It is NOT a human-provisioned
secret — it is base64 of 'application:email' (here 'subsets:nathan@subsets.io'),
self-generated via the API's own /encode_app_identifier endpoint.
"""

import json

from subsets_utils import NodeSpec, get, raw_writer, transient_retry

from constants import ENTITY_IDS, ENTITY_PATHS

BASE_URL = "https://hapi.humdata.org/api/v2"
# Self-generated, non-secret app identifier: base64("subsets:nathan@subsets.io").
APP_IDENTIFIER = "c3Vic2V0czpuYXRoYW5Ac3Vic2V0cy5pbw=="
PAGE_SIZE = 10000          # server caps limit at 10000 (422s above)
MAX_PAGES = 5000           # safety ceiling (→ 50M rows); raises, never silent


@transient_retry()  # 6 attempts, exp backoff over transient net errors + 429 + 5xx
def _fetch_page(url: str, offset: int) -> list:
    resp = get(
        url,
        params={
            "app_identifier": APP_IDENTIFIER,
            "output_format": "json",
            "limit": PAGE_SIZE,
            "offset": offset,
        },
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()["data"]


def fetch_one(node_id: str) -> None:
    """Page one HAPI v2 endpoint to exhaustion and write it as NDJSON.

    The runtime passes the spec id; it IS the asset name. The entity (and thus
    the endpoint path) is recovered by stripping the 'ocha-' prefix.
    """
    asset = node_id
    entity = node_id[len("ocha-"):]
    url = f"{BASE_URL}/{ENTITY_PATHS[entity]}"

    offset = 0
    pages = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as w:
        while True:
            page = _fetch_page(url, offset)
            for row in page:
                w.write(json.dumps(row) + "\n")
            pages += 1
            if len(page) < PAGE_SIZE:
                break
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{asset}: hit MAX_PAGES={MAX_PAGES} at offset={offset}; "
                    "source grew past expectations — raise the ceiling deliberately"
                )
            offset += PAGE_SIZE


DOWNLOAD_SPECS = [
    NodeSpec(id=f"ocha-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
