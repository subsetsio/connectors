"""Shared HTTP/retry helpers for the FAA connector.

The FAA edge WAF 403s requests without a browser User-Agent, so configure_http
sets one. Both fetch mechanisms (Aircraft Registry ZIP and AIS ArcGIS
FeatureServers) go through faa_get.
"""

from subsets_utils import configure_http, get, transient_retry

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


@transient_retry()
def faa_get(url: str, **kwargs):
    # The FAA WAF needs a browser UA; set it once per process.
    configure_http(headers={"User-Agent": _UA, "Referer": "https://www.faa.gov/"})
    resp = get(url, timeout=(15.0, 300.0), **kwargs)
    resp.raise_for_status()
    return resp
