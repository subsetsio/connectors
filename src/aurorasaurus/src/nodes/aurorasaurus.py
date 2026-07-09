"""Aurorasaurus connector — crowd-sourced aurora sighting reports.

Single subset: the live /web-obs/list REST feed (Django REST Framework,
page/page_size/count/next/previous/results envelope), ~41,705 reports.

Fetch shape: stateless full re-pull. The corpus is small (~tens of MB) and
the documented date filters are unreliable (they bind time_start/time_end —
user-entered, frequently garbage — not the submission `timestamp`), so there
is no usable incremental cursor. We page the whole corpus every refresh and
overwrite; late edits and re-verifications are picked up for free. Raw is
written as a single NDJSON asset because records are nested (location struct,
observer struct) and several fields drift between null / scalar / list.
"""

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

BASE_URL = "https://www.aurorasaurus.org/web-obs/list"
PAGE_SIZE = 200            # server silently caps any larger request at 200
MAX_PAGES = 2000           # safety ceiling (~400k records); raises if exceeded


def _fetch_page(page: int) -> dict:
    resp = get(
        BASE_URL,
        params={"page": page, "page_size": PAGE_SIZE},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_web_observations(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    rows: list[dict] = []
    page = 1
    while True:
        if page > MAX_PAGES:
            raise RuntimeError(
                f"{asset}: exceeded MAX_PAGES={MAX_PAGES} — source grew past "
                f"expectations or pagination is looping; refusing to truncate silently"
            )
        payload = _fetch_page(page)
        batch = payload.get("results") or []
        rows.extend(batch)
        if not payload.get("next"):
            break
        page += 1

    if not rows:
        raise RuntimeError(f"{asset}: fetched 0 rows across {page} page(s)")

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="aurorasaurus-web-observations",
        fn=fetch_web_observations,
        kind="download",
    ),
]
