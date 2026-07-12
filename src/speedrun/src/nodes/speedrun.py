"""Speedrun.com REST API connector.

Downloads are stateless full snapshots from the public v1 JSON API. The API has
offset pagination and a documented 100 requests/minute/IP throttle, so the
fetcher uses one shared paginated path and paces requests below that limit.

Raw is compressed NDJSON because API records contain nested structures and
resource schemas differ. The large `runs` corpus is streamed line-by-line rather
than accumulated in memory.
"""

from __future__ import annotations

import json
import time
from collections.abc import Iterator
from urllib.parse import parse_qs, urlparse

from subsets_utils import MaintainSpec, NodeSpec, get, raw_asset_exists, raw_writer

BASE_URL = "https://www.speedrun.com/api/v1"
REQUEST_DELAY_SECONDS = 0.7  # stay under the documented 100 requests/min/IP

RESOURCE_CONFIG = {
    "games": {
        "path": "/games",
        "params": {"_bulk": "yes", "max": 1000},
    },
    "platforms": {
        "path": "/platforms",
        "params": {"max": 200},
    },
    "regions": {
        "path": "/regions",
        "params": {"max": 200},
    },
    "runs": {
        "path": "/runs",
        "params": {"max": 200, "orderby": "verify-date", "direction": "desc"},
        # The API returns HTTP 400 once offset reaches 10000 on /runs.
        # Keep the newest 10k submissions rather than failing the whole asset.
        "max_offset_exclusive": 10000,
    },
    "series": {
        "path": "/series",
        "params": {"max": 200},
    },
}

GAME_CHILD_RESOURCES = {
    "categories": "categories",
    "levels": "levels",
    "variables": "variables",
}

GAMES_WITH_EMBEDS_PARAMS = {
    "max": 200,
    "embed": "categories,levels,variables",
}

LEADERBOARD_RECORD_GAME_LIMIT = 500


def _entity_from_node_id(node_id: str) -> str:
    prefix = "speedrun-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id: {node_id}")
    return node_id[len(prefix):].replace("-", "_")


def _fetch_page(url: str, params: dict | None) -> dict:
    resp = get(url, params=params, timeout=(15.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _next_url(payload: dict) -> str | None:
    pagination = payload.get("pagination")
    if not isinstance(pagination, dict):
        return None
    for link in pagination.get("links") or []:
        if link.get("rel") == "next":
            return link.get("uri")
    return None


def _offset_from_url(url: str) -> int | None:
    parsed = urlparse(url)
    values = parse_qs(parsed.query).get("offset")
    if not values:
        return None
    try:
        return int(values[0])
    except ValueError:
        return None


def _iter_resource(entity: str) -> Iterator[dict]:
    config = RESOURCE_CONFIG[entity]
    url = BASE_URL + config["path"]
    params = dict(config["params"])
    page = 0

    while url:
        payload = _fetch_page(url, params)
        rows = payload.get("data") or []
        if not isinstance(rows, list):
            raise RuntimeError(f"{entity}: expected list data, got {type(rows).__name__}")
        if page == 0 and not rows:
            raise RuntimeError(f"{entity}: first page returned 0 rows")

        fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for row in rows:
            if not isinstance(row, dict):
                raise RuntimeError(f"{entity}: non-object row {row!r}")
            out = dict(row)
            out["_fetched_at"] = fetched_at
            out["_resource"] = entity
            out["_page"] = page
            yield out

        url = _next_url(payload)
        if url and (cap := config.get("max_offset_exclusive")) is not None:
            next_offset = _offset_from_url(url)
            if next_offset is not None and next_offset >= cap:
                break
        params = None  # next links already carry query params
        page += 1
        if url:
            time.sleep(REQUEST_DELAY_SECONDS)


def _iter_games_with_embeds() -> Iterator[dict]:
    url = BASE_URL + "/games"
    params = dict(GAMES_WITH_EMBEDS_PARAMS)
    page = 0

    while url:
        payload = _fetch_page(url, params)
        rows = payload.get("data") or []
        if not isinstance(rows, list):
            raise RuntimeError(f"games embeds: expected list data, got {type(rows).__name__}")
        if page == 0 and not rows:
            raise RuntimeError("games embeds: first page returned 0 rows")

        for row in rows:
            if not isinstance(row, dict):
                raise RuntimeError(f"games embeds: non-object row {row!r}")
            yield row

        url = _next_url(payload)
        params = None
        page += 1
        if url:
            time.sleep(REQUEST_DELAY_SECONDS)


def _iter_game_child_resource(entity: str) -> Iterator[dict]:
    embed_key = GAME_CHILD_RESOURCES[entity]
    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    for game in _iter_games_with_embeds():
        game_id = game.get("id")
        embedded = game.get(embed_key) or {}
        rows = embedded.get("data") or []
        if not isinstance(rows, list):
            raise RuntimeError(f"{entity}: embedded data for game {game_id} is not a list")

        for row in rows:
            if not isinstance(row, dict):
                raise RuntimeError(f"{entity}: non-object row {row!r}")
            out = dict(row)
            out["_fetched_at"] = fetched_at
            out["_resource"] = entity
            out["_game"] = game_id
            out["_game_abbreviation"] = game.get("abbreviation")
            yield out


def _iter_bulk_games(limit: int | None = None) -> Iterator[dict]:
    url = BASE_URL + "/games"
    params = {"_bulk": "yes", "max": 1000}
    count = 0
    page = 0

    while url:
        payload = _fetch_page(url, params)
        rows = payload.get("data") or []
        if not isinstance(rows, list):
            raise RuntimeError(f"bulk games: expected list data, got {type(rows).__name__}")
        if page == 0 and not rows:
            raise RuntimeError("bulk games: first page returned 0 rows")

        for row in rows:
            if not isinstance(row, dict):
                raise RuntimeError(f"bulk games: non-object row {row!r}")
            yield row
            count += 1
            if limit is not None and count >= limit:
                return

        url = _next_url(payload)
        params = None
        page += 1
        if url:
            time.sleep(REQUEST_DELAY_SECONDS)


def _iter_leaderboard_records() -> Iterator[dict]:
    fetched_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    for game in _iter_bulk_games(limit=LEADERBOARD_RECORD_GAME_LIMIT):
        game_id = game["id"]
        payload = _fetch_page(f"{BASE_URL}/games/{game_id}/records", {"top": 1})
        rows = payload.get("data") or []
        if not isinstance(rows, list):
            raise RuntimeError(f"leaderboard_records: expected list data for game {game_id}")

        for row in rows:
            if not isinstance(row, dict):
                raise RuntimeError(f"leaderboard_records: non-object row {row!r}")
            out = dict(row)
            out["_fetched_at"] = fetched_at
            out["_resource"] = "leaderboard_records"
            out["_game"] = game_id
            out["_game_abbreviation"] = game.get("abbreviation")
            yield out

        time.sleep(REQUEST_DELAY_SECONDS)


def fetch_resource(node_id: str) -> None:
    entity = _entity_from_node_id(node_id)
    if entity not in RESOURCE_CONFIG:
        raise ValueError(f"no resource config for {entity!r}")

    count = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as f:
        for row in _iter_resource(entity):
            f.write(json.dumps(row, separators=(",", ":")) + "\n")
            count += 1

    if count == 0:
        raise RuntimeError(f"{node_id}: wrote 0 rows")
    print(f"{node_id}: wrote {count:,} rows")


def fetch_game_child_resource(node_id: str) -> None:
    entity = _entity_from_node_id(node_id)
    if entity not in GAME_CHILD_RESOURCES:
        raise ValueError(f"no game child resource config for {entity!r}")

    count = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as f:
        for row in _iter_game_child_resource(entity):
            f.write(json.dumps(row, separators=(",", ":")) + "\n")
            count += 1

    if count == 0:
        raise RuntimeError(f"{node_id}: wrote 0 rows")
    print(f"{node_id}: wrote {count:,} rows")


def fetch_leaderboard_records(node_id: str) -> None:
    count = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as f:
        for row in _iter_leaderboard_records():
            f.write(json.dumps(row, separators=(",", ":")) + "\n")
            count += 1

    if count == 0:
        raise RuntimeError(f"{node_id}: wrote 0 rows")
    print(f"{node_id}: wrote {count:,} rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="speedrun-categories", fn=fetch_game_child_resource, kind="download"),
    NodeSpec(id="speedrun-games", fn=fetch_resource, kind="download"),
    NodeSpec(id="speedrun-leaderboard-records", fn=fetch_leaderboard_records, kind="download"),
    NodeSpec(id="speedrun-levels", fn=fetch_game_child_resource, kind="download"),
    NodeSpec(id="speedrun-platforms", fn=fetch_resource, kind="download"),
    NodeSpec(id="speedrun-regions", fn=fetch_resource, kind="download"),
    NodeSpec(id="speedrun-runs", fn=fetch_resource, kind="download"),
    NodeSpec(id="speedrun-series", fn=fetch_resource, kind="download"),
    NodeSpec(id="speedrun-variables", fn=fetch_game_child_resource, kind="download"),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Refresh weekly; Speedrun.com API is live community data with no "
            "published release schedule, cadence inferred from active verified "
            "runs and documented API cache windows."
        ),
        check=lambda aid: raw_asset_exists(aid, "ndjson.gz", max_age_days=7),
    )
    for spec in DOWNLOAD_SPECS
]
