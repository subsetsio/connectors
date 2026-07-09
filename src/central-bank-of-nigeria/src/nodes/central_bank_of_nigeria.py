"""Central Bank of Nigeria (cbn) connector — download stage.

Source: the CBN public JSON REST API at https://www.cbn.gov.ng/api/ that powers
the bank's "Data & Statistics" pages (/rates/*.html). Each accepted dataset is
exposed as one `GetAll<Dataset>` endpoint returning the FULL time series as a
single flat JSON array (no pagination, no auth). Numeric values come back as JSON
strings (missing values as ""), so the model/transform stage casts and cleans.

Fetch shape: stateless full re-pull. Every endpoint returns the entire series in
one request (largest observed ~18k daily rows / a few MB; whole corpus well under
100MB), so we re-fetch the whole corpus each run and overwrite — revisions and
late corrections are picked up for free. The source exposes no incremental filter
(no since/cursor/modifiedAfter), so incremental is not possible; full re-pull is
cheap enough that it doesn't matter.

Raw is written as NDJSON: column sets differ per dataset and every value arrives
as a string (missing = ""), so there is no stable cross-record schema worth
declaring in parquet — the SQL transform re-types on read.
"""
from subsets_utils import (
    NodeSpec,
    configure_http,
    get,
    save_raw_ndjson,
    transient_retry,
)

from constants import ENDPOINTS

SLUG = "central-bank-of-nigeria"
PREFIX = SLUG + "-"
API_BASE = "https://www.cbn.gov.ng/api/"

# The host sits behind Cloudflare, which serves a challenge to non-browser
# agents; present a normal desktop-browser User-Agent. ASCII only.
_BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


@transient_retry()
def _fetch_json(url: str):
    # ?format=json is required on some endpoints (e.g. GetAllInterbankRates,
    # which otherwise returns XML) and harmless on the rest.
    resp = get(
        url,
        params={"format": "json"},
        headers={"Accept": "application/json"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    configure_http(headers={"User-Agent": _BROWSER_UA})
    entity_id = node_id.removeprefix(PREFIX)
    endpoint = ENDPOINTS[entity_id]
    data = _fetch_json(API_BASE + endpoint)
    if not isinstance(data, list):
        raise TypeError(
            f"{entity_id}: expected a JSON array from {endpoint}, "
            f"got {type(data).__name__}"
        )
    save_raw_ndjson(data, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{entity_id}", fn=fetch_one, kind="download")
    for entity_id in ENDPOINTS
]
