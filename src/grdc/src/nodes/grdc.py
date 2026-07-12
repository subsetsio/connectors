"""GRDC — Global Runoff Data Centre station catalogue.

Single bulk JSON file (the complete ~11,879-station catalogue) published as one
Delta table. The actual discharge time series are NOT freely available (gated
behind a manual request/email-approval workflow), so this station catalogue —
identity, location, catchment area and discharge summary statistics per gauging
station — is the publishable statistical product.

Stateless full re-pull: the whole corpus is one ~9MB JSON GET, so we re-fetch
the entire file every run and overwrite. Raw is saved as NDJSON because column
types drift across records (e.g. `area` is int or float, period fields are
float-or-null, `*_day`/`*_month` are int-or-empty-string); the transform
re-types and cleans sentinel values (-999 = missing).
"""

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

CATALOGUE_URL = "https://portal.grdc.bafg.de/grdc/grdc_sample_records.json"


@transient_retry()
def _fetch_catalogue() -> list:
    # subsets_utils.get sets a browser-like User-Agent (verified to return 200;
    # the bafg portal 400s the default curl UA). Full corpus in one response.
    resp = get(CATALOGUE_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise TypeError(f"expected a JSON array, got {type(data).__name__}")
    return data


def fetch_station_catalogue(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    rows = _fetch_catalogue()
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="grdc-station-catalogue", fn=fetch_station_catalogue, kind="download"),
]
