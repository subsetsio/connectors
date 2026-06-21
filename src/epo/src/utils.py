"""Shared HTTP helper for the EPO Statistics & Trends Centre connector.

The corpus is five public, no-auth JSON files served under
https://www.epo.org/sites/default/files/stc_centre/statistic_centre_data/json-data/.
Every subset fetcher re-pulls its file via `fetch_json` below.
"""

from subsets_utils import get, transient_retry

BASE = "https://www.epo.org/sites/default/files/stc_centre/statistic_centre_data/json-data"

# The static asset endpoints are Cloudflare-fronted; the plain HTML pages are
# challenged, but the /sites/default/files/ assets serve to a normal browser UA.
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


@transient_retry()
def fetch_json(filename: str):
    resp = get(
        f"{BASE}/{filename}",
        headers={"User-Agent": UA},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()
