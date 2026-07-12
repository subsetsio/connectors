"""UK Parliament public data APIs.

The official developer hub exposes several unauthenticated REST APIs. Each
accepted collect entity maps to one primary list/search endpoint and is fetched
as a full snapshot with offset pagination. Raw is NDJSON because responses carry
nested people, parties, links, teller lists, and other fields that drift across
API families.
"""
from __future__ import annotations

import time
from collections.abc import Iterable

from subsets_utils import NodeSpec, get, save_raw_ndjson

SLUG = "uk-parliament"

PAGE_CONFIGS = {
    "bills": {
        "url": "https://bills-api.parliament.uk/api/v1/Bills",
        "skip_param": "Skip",
        "take_param": "Take",
        "page_size": 100,
        "items_path": ("items",),
        "total_path": ("totalResults",),
    },
    "committees": {
        "url": "https://committees-api.parliament.uk/api/Committees",
        "skip_param": "Skip",
        "take_param": "Take",
        "page_size": 100,
        "items_path": ("items",),
        "total_path": ("totalResults",),
    },
    "erskine-may": {
        "url": "https://erskinemay-api.parliament.uk/api/Part",
        "items_path": (),
        "total_path": None,
        "endpoint": "parts",
    },
    "commons-votes": {
        "url": "https://commonsvotes-api.parliament.uk/data/divisions.json/search",
        "skip_param": "queryParameters.skip",
        "take_param": "queryParameters.take",
        "page_size": 100,
        "items_path": (),
        "total_path": None,
    },
    "interests": {
        "url": "https://interests-api.parliament.uk/api/v1/Interests",
        "skip_param": "Skip",
        "take_param": "Take",
        "page_size": 100,
        "items_path": ("items",),
        "total_path": ("totalResults",),
        "extra_params": {"ExpandChildInterests": "False"},
    },
    "lords-votes": {
        "url": "https://lordsvotes-api.parliament.uk/data/Divisions/search",
        "skip_param": "skip",
        "take_param": "take",
        "page_size": 100,
        "items_path": (),
        "total_path": None,
    },
    "members": {
        "url": "https://members-api.parliament.uk/api/Members/Search",
        "skip_param": "skip",
        "take_param": "take",
        "page_size": 100,
        "items_path": ("items",),
        "total_path": ("totalResults",),
    },
    "oral-questions-and-motions": {
        "url": "https://oralquestionsandmotions-api.parliament.uk/oralquestions/list",
        "skip_param": "parameters.skip",
        "take_param": "parameters.take",
        "page_size": 100,
        "items_path": ("Response",),
        "total_path": ("PagingInfo", "Total"),
    },
    "parliament-now": {
        "url": "https://now-api.parliament.uk/api/Message/message/Commons/current",
        "items_path": None,
        "total_path": None,
        "endpoint": "commons-current",
    },
    "statutory-instruments": {
        "url": "https://statutoryinstruments-api.parliament.uk/api/v2/StatutoryInstrument",
        "skip_param": "Skip",
        "take_param": "Take",
        "page_size": 100,
        "items_path": ("items",),
        "total_path": ("totalResults",),
    },
    "treaties": {
        "url": "https://treaties-api.parliament.uk/api/Treaty",
        "skip_param": "Skip",
        "take_param": "Take",
        "page_size": 100,
        "items_path": ("items",),
        "total_path": ("totalResults",),
    },
    "written-questions-and-statements": [
        {
            "url": "https://questions-statements-api.parliament.uk/api/dailyreports/dailyreports",
            "skip_param": "skip",
            "take_param": "take",
            "page_size": 100,
            "items_path": ("results",),
            "total_path": ("totalResults",),
            "endpoint": "dailyreports",
        },
        {
            "url": "https://questions-statements-api.parliament.uk/api/writtenstatements/statements",
            "skip_param": "skip",
            "take_param": "take",
            "page_size": 100,
            "items_path": ("results",),
            "total_path": ("totalResults",),
            "endpoint": "writtenstatements",
        },
    ],
}


EXTRA_PAGE_CONFIGS = {
    "erskine-may": [
        {
            "url": "https://erskinemay-api.parliament.uk/api/IndexTerm/browse",
            "skip_param": "skip",
            "take_param": "take",
            "page_size": 100,
            "items_path": ("searchResults",),
            "total_path": ("totalResults",),
            "endpoint": "index-terms",
        }
    ],
    "parliament-now": [
        {
            "url": "https://now-api.parliament.uk/api/Message/message/Lords/current",
            "items_path": None,
            "total_path": None,
            "endpoint": "lords-current",
        }
    ],
}


MAINTENANCE_URLS = {
    "bills": "https://bills-api.parliament.uk/swagger/v1/swagger.json",
    "committees": "https://committees-api.parliament.uk/swagger/v1/swagger.json",
    "commons-votes": "https://commonsvotes-api.parliament.uk/swagger/docs/v1",
    "erskine-may": "https://erskinemay-api.parliament.uk/swagger/v1/swagger.json",
    "interests": "https://interests-api.parliament.uk/swagger/v1/swagger.json",
    "lords-votes": "https://lordsvotes-api.parliament.uk/swagger/v1/swagger.json",
    "members": "https://members-api.parliament.uk/swagger/v1/swagger.json",
    "oral-questions-and-motions": "https://oralquestionsandmotions-api.parliament.uk/swagger/docs/v1",
    "parliament-now": "https://now-api.parliament.uk/swagger/v1/swagger.json",
    "statutory-instruments": "https://statutoryinstruments-api.parliament.uk/swagger/v2/swagger.json",
    "treaties": "https://treaties-api.parliament.uk/swagger/v1/swagger.json",
    "written-questions-and-statements": "https://questions-statements-api.parliament.uk/swagger/v1/swagger.json",
}


def _entity_id_from_node(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id[len(prefix):]


def _get_path(data, path: tuple[str, ...] | None):
    if path is None:
        return None
    current = data
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _items_from_payload(payload, path: tuple[str, ...] | None) -> list:
    if path is None:
        return [payload]
    items = payload if not path else _get_path(payload, path)
    if items is None:
        return []
    if not isinstance(items, list):
        raise TypeError(f"expected list at {'.'.join(path) or '<root>'}, got {type(items).__name__}")
    return items


def _normalize_row(row, entity_id: str, skip: int, endpoint: str) -> dict:
    if not isinstance(row, dict):
        row = {"value": row}
    return {
        "source_entity": entity_id,
        "source_endpoint": endpoint,
        "source_skip": skip,
        "record": row,
    }


def _rows_for_config(entity_id: str, config: dict) -> Iterable[dict]:
    skip = 0
    page_size = config.get("page_size")
    endpoint = config.get("endpoint") or entity_id
    total = None

    while True:
        params = dict(config.get("extra_params", {}))
        if page_size is not None:
            params[config["skip_param"]] = skip
            params[config["take_param"]] = page_size
        resp = get(config["url"], params=params, timeout=(10.0, 180.0))
        resp.raise_for_status()
        payload = resp.json()
        items = _items_from_payload(payload, config["items_path"])
        if total is None:
            total = _get_path(payload, config["total_path"])
            if isinstance(total, str) and total.isdigit():
                total = int(total)

        for row in items:
            yield _normalize_row(row, entity_id, skip, endpoint)

        if page_size is None:
            break
        if not items:
            break
        skip += len(items)
        if isinstance(total, int) and skip >= total:
            break
        if len(items) < page_size and total is None:
            break
        time.sleep(0.05)


def _paged_rows(entity_id: str) -> Iterable[dict]:
    configs = PAGE_CONFIGS[entity_id]
    if isinstance(configs, dict):
        configs = [configs]
    configs = [*configs, *EXTRA_PAGE_CONFIGS.get(entity_id, [])]
    for config in configs:
        yield from _rows_for_config(entity_id, config)


def fetch_one(node_id: str) -> None:
    entity_id = _entity_id_from_node(node_id)
    rows = list(_paged_rows(entity_id))
    if not rows:
        raise RuntimeError(f"{node_id}: fetched 0 rows from {entity_id}")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity_id}", fn=fetch_one, kind="download")
    for entity_id in PAGE_CONFIGS
]
