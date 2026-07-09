"""Shared HTTP + paging helpers for the data.gov CKAN connector.

The catalog is served keyless and unthrottled at catalog-old.data.gov (the
api.gsa.gov gateway requires an api.data.gov key we don't have). `_action`
wraps the CKAN action API with transient retry and success-flag checking;
`_crawl_packages` pages the full package corpus once, writing one ndjson batch
per page so peak memory stays at a single page. Shared by the datasets and
resources download nodes (both crawl the same package payload).
"""

from subsets_utils import get, save_raw_ndjson, transient_retry

BASE = "https://catalog-old.data.gov/api/3"
PAGE_SIZE = 1000          # CKAN/Solr caps rows at 1000 (verified)
SORT = "metadata_created asc"  # stable-ish order for start/rows deep paging
MAX_PAGES = 2000          # safety ceiling (~403 expected); raises if exceeded


@transient_retry(attempts=8, min_wait=8, max_wait=180)
def _action(action: str, **params) -> dict:
    resp = get(f"{BASE}/action/{action}", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    body = resp.json()
    if not body.get("success", False):
        raise RuntimeError(f"CKAN action {action} returned success=false: {str(body)[:200]}")
    return body["result"]


def _crawl_packages(node_id: str, row_builder) -> None:
    """Page the full package corpus, writing one ndjson batch per page.

    row_builder(pkg) -> list[dict] (resources) or [dict] (datasets).
    """
    first = _action("package_search", rows=PAGE_SIZE, start=0, sort=SORT)
    count = first["count"]
    start = 0
    page = 0
    results = first["results"]
    while results:
        batch: list[dict] = []
        for pkg in results:
            batch.extend(row_builder(pkg))
        if batch:
            save_raw_ndjson(batch, node_id, fragment=f"{page:05d}")
        start += len(results)
        page += 1
        if page > MAX_PAGES:
            raise RuntimeError(
                f"{node_id}: exceeded MAX_PAGES={MAX_PAGES} (count={count}, start={start}) "
                "— source grew past expectations or paging is looping"
            )
        if start >= count:
            break
        results = _action("package_search", rows=PAGE_SIZE, start=start, sort=SORT)["results"]
