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
DETAIL_SLEEP_SECONDS = 1.1


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


def _iter_all_apps() -> list[dict]:
    apps_by_id = {}
    page = 0

    while True:
        page_payload = _get_all_page(page)
        if not page_payload:
            break

        for appid, record in page_payload.items():
            if not isinstance(record, dict):
                continue
            row = dict(record)
            appid_int = int(row.get("appid") or appid)
            if appid_int in apps_by_id:
                continue
            row["appid"] = appid_int
            row["source_page"] = page
            apps_by_id[appid_int] = row

        if len(page_payload) < 1000:
            break

        page += 1
        time.sleep(PAGE_SLEEP_SECONDS)

    return sorted(apps_by_id.values(), key=lambda row: row["appid"])


def fetch_apps(node_id: str) -> None:
    save_raw_ndjson(_iter_all_apps(), node_id)


def _get_app_details(appid: int) -> dict:
    response = get(
        BASE_URL,
        params={"request": "appdetails", "appid": appid},
        headers={"Accept": "application/json"},
        timeout=(10.0, 120.0),
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise TypeError(f"expected dict appdetails payload for {appid}, got {type(payload).__name__}")
    return payload


def fetch_app_tags(node_id: str) -> None:
    rows = []
    apps = _iter_all_apps()

    for index, app in enumerate(apps):
        if index:
            time.sleep(DETAIL_SLEEP_SECONDS)
        details = _get_app_details(app["appid"])
        tags = details.get("tags") or {}
        if not isinstance(tags, dict):
            continue
        for tag, votes in tags.items():
            rows.append(
                {
                    "appid": int(app["appid"]),
                    "name": str(details.get("name") or app.get("name") or ""),
                    "tag": str(tag),
                    "votes": int(votes or 0),
                }
            )

    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="steam-spy-app-tags", fn=fetch_app_tags),
    NodeSpec(id="steam-spy-apps", fn=fetch_apps),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="steam-spy-app-tags",
        description=(
            "Steam Spy says data refreshes once daily and appdetails requests should "
            "not be repeated more than once every 24 hours; skip raw assets younger than 1 day."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "ndjson.zst", max_age_days=1),
    ),
    MaintainSpec(
        asset_id="steam-spy-apps",
        description=(
            "Steam Spy says data refreshes once daily and all requests should not be "
            "repeated more than once every 24 hours; skip raw assets younger than 1 day."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "ndjson.zst", max_age_days=1),
    ),
]
