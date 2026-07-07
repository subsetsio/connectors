"""Download nodes for Steam Spy.

Steam Spy exposes one public REST endpoint. The full-corpus path is
request=all, paged in 1000-app chunks, with a documented cap of one all
request per 60 seconds. The source refreshes daily, so the maintain policy
skips fresh local raw assets and the fetch function remains an unconditional
full snapshot when invoked.
"""

import time

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    save_raw_ndjson,
)

BASE_URL = "https://steamspy.com/api.php"
PAGE_SLEEP_SECONDS = 61


def _get_all_page(page: int) -> dict:
    response = get(
        BASE_URL,
        params={"request": "all", "page": page},
        headers={"Accept": "application/json"},
        timeout=(10.0, 120.0),
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise TypeError(f"expected dict payload for page {page}, got {type(payload).__name__}")
    return payload


def fetch_apps(node_id: str) -> None:
    rows = []
    page = 0

    while True:
        page_payload = _get_all_page(page)
        if not page_payload:
            break

        for appid, record in page_payload.items():
            if not isinstance(record, dict):
                continue
            row = dict(record)
            row["appid"] = int(row.get("appid") or appid)
            row["source_page"] = page
            rows.append(row)

        if len(page_payload) < 1000:
            break

        page += 1
        time.sleep(PAGE_SLEEP_SECONDS)

    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="steam-spy-apps", fn=fetch_apps),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="steam-spy-apps",
        description=(
            "Steam Spy says data refreshes once daily and all requests should not be "
            "repeated more than once every 24 hours; skip raw assets younger than 1 day."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "ndjson.zst", max_age_days=1),
    ),
]
