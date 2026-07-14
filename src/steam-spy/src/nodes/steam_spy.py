"""Download nodes for Steam Spy.

Steam Spy exposes one public REST endpoint. The full-corpus path is
request=all, paged in 1000-app chunks, with a documented cap of one all
request per 60 seconds. The source refreshes daily, so the maintain policy
skips fresh local raw assets and the fetch function remains an unconditional
full snapshot when invoked.
"""

import os
import time

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    list_raw_fragments,
    load_state,
    raw_asset_exists,
    save_raw_ndjson,
    save_state,
)

BASE_URL = "https://steamspy.com/api.php"
PAGE_SLEEP_SECONDS = 61
DETAIL_SLEEP_SECONDS = 1.1
TAG_BATCH_SIZE = int(os.environ.get("STEAM_SPY_TAG_BATCH_SIZE", "250"))
TAG_LEG_SECONDS = int(os.environ.get("STEAM_SPY_TAG_LEG_SECONDS", str(5 * 60 * 60)))
STATE_VERSION = 2


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


def _appid_universe(node_id: str, run_id: str) -> list[int]:
    state = load_state(node_id)
    if (
        state.get("schema_version") == STATE_VERSION
        and state.get("run_id") == run_id
        and isinstance(state.get("appids"), list)
    ):
        return [int(appid) for appid in state["appids"]]

    apps = _iter_all_apps()
    appids = [int(app["appid"]) for app in apps]
    save_state(
        node_id,
        {
            "schema_version": STATE_VERSION,
            "run_id": run_id,
            "total_apps": len(appids),
            "appids": appids,
        },
    )
    return appids


def _completed_tag_batches(node_id: str, run_id: str) -> set[int]:
    completed = set()
    for fragment, meta in list_raw_fragments(node_id, "ndjson.zst").items():
        if meta.get("run_id") != run_id or not fragment.startswith("batch-"):
            continue
        try:
            completed.add(int(fragment.removeprefix("batch-")))
        except ValueError:
            continue
    return completed


def _tag_rows_for_app(appid: int) -> list[dict]:
    details = _get_app_details(appid)
    tags = details.get("tags") or {}
    if not isinstance(tags, dict):
        return []
    name = str(details.get("name") or "")
    rows = []
    for tag, votes in tags.items():
        rows.append(
            {
                "appid": int(appid),
                "name": name,
                "tag": str(tag),
                "votes": int(votes or 0),
            }
        )
    return rows


def fetch_app_tags(node_id: str):
    run_id = os.environ.get("RUN_ID", "unknown")
    deadline = time.monotonic() + TAG_LEG_SECONDS
    appids = _appid_universe(node_id, run_id)
    completed = _completed_tag_batches(node_id, run_id)
    total_batches = (len(appids) + TAG_BATCH_SIZE - 1) // TAG_BATCH_SIZE

    for batch_index in range(total_batches):
        if batch_index in completed:
            continue
        if time.monotonic() >= deadline:
            print(
                f"{node_id}: leg budget spent with "
                f"{len(completed)}/{total_batches} batches complete; requesting continuation"
            )
            return True

        start = batch_index * TAG_BATCH_SIZE
        batch_appids = appids[start:start + TAG_BATCH_SIZE]
        rows = []
        for offset, appid in enumerate(batch_appids):
            if offset:
                time.sleep(DETAIL_SLEEP_SECONDS)
            rows.extend(_tag_rows_for_app(appid))

        fragment = f"batch-{batch_index:05d}"
        save_raw_ndjson(rows, node_id, fragment=fragment)
        completed.add(batch_index)
        save_state(
            node_id,
            {
                "schema_version": STATE_VERSION,
                "run_id": run_id,
                "total_apps": len(appids),
                "total_batches": total_batches,
                "completed_batches": len(completed),
                "appids": appids,
            },
        )
        print(
            f"{node_id}: wrote {len(rows)} tag rows for "
            f"batch {batch_index + 1}/{total_batches}"
        )

    print(f"{node_id}: all {total_batches} tag batches complete")


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
