"""CISA Known Exploited Vulnerabilities (KEV) catalog connector.

Single-entity, stateless full re-pull: the entire KEV catalog (~1600 CVEs, ~4MB)
is served from one stable JSON URL and re-fetched in full each run. No incremental
filter exists and the corpus is tiny, so we overwrite the published table every run
— late corrections and re-categorizations are picked up for free.
"""


from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

FEED_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


@transient_retry()
def _fetch_catalog() -> dict:
    resp = get(FEED_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def fetch_kev(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    catalog = _fetch_catalog()
    vulns = catalog.get("vulnerabilities", [])
    if not vulns:
        raise AssertionError("KEV feed returned no vulnerabilities")
    catalog_version = catalog.get("catalogVersion")
    date_released = catalog.get("dateReleased")
    # Stamp each record with catalog-level provenance so the published table
    # carries the version/release it came from.
    rows = [
        {**v, "catalogVersion": catalog_version, "dateReleased": date_released}
        for v in vulns
    ]
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="cisa-kev-known-exploited-vulnerabilities", fn=fetch_kev, kind="download"),
]

# Transforms are authored as file pairs under src/transforms/ (SQL + YAML contract).
