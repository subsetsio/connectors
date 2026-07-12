"""Statistics Iceland PX-Web catalog connector.

Each rank-accepted Statistics Iceland table is downloaded as one raw NDJSON
asset. The fetcher expands PX-Web json-stat2 cubes into long rows: one column
per table dimension, plus ``obs_value`` and ``obs_time`` when the source marks a
time dimension.
"""

import json
import re
import time
import urllib.parse

from subsets_utils import MaintainSpec, NodeSpec, get, post, raw_asset_exists, raw_writer
from constants import ENTITY_IDS, ENTITY_NAMES, ENTITY_PATHS, ENTITY_UPDATED


BASE = "https://px.hagstofa.is/pxen/api/v1/en"
SLUG = "statice"
MAX_CELLS = 80_000
MAX_VALUES = 4_900
PACE_SECONDS = 0.15
MAINTAIN_MAX_AGE_DAYS = 7


def _url_for(entity: str) -> str:
    return BASE + "".join(
        "/" + urllib.parse.quote(part, safe="")
        for part in ENTITY_PATHS[entity]
    )


def _throttle() -> None:
    time.sleep(PACE_SECONDS)


def _get_json(url: str):
    _throttle()
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _post_json(url: str, query: dict):
    _throttle()
    resp = post(url, json=query, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _sanitize(text: str, used: set[str]) -> str:
    name = re.sub(r"[^0-9a-z]+", "_", text.strip().lower()).strip("_") or "dim"
    if name in {"obs_value", "obs_time", "table_id", "value"}:
        name = f"{name}_dim"
    base = name
    i = 2
    while name in used:
        name = f"{base}_{i}"
        i += 1
    used.add(name)
    return name


def _resolve_values(url: str, variables: list[dict]) -> dict[str, list[str]]:
    resolved: dict[str, list[str]] = {}
    empty = []
    for var in variables:
        values = var.get("values") or []
        if values:
            resolved[var["code"]] = list(values)
        else:
            empty.append(var["code"])

    for target in empty:
        query = {"query": [], "response": {"format": "json-stat2"}}
        for var in variables:
            code = var["code"]
            if code == target:
                selection = {"filter": "all", "values": ["*"]}
            elif resolved.get(code):
                selection = {"filter": "item", "values": [resolved[code][0]]}
            else:
                selection = {"filter": "top", "values": ["1"]}
            query["query"].append({"code": code, "selection": selection})
        doc = _post_json(url, query)
        index = doc["dimension"][target]["category"]["index"]
        if isinstance(index, dict):
            values = [None] * len(index)
            for value, pos in index.items():
                values[pos] = value
            resolved[target] = values
        else:
            resolved[target] = list(index)
    return resolved


def _cell_count(block: dict[str, list[str]]) -> int:
    total = 1
    for values in block.values():
        total *= max(1, len(values))
    return total


def _plan_blocks(resolved: dict[str, list[str]]) -> list[dict[str, list[str]]]:
    blocks = [{code: list(values) for code, values in resolved.items()}]
    ready = []
    guard = 0
    while blocks:
        guard += 1
        if guard > 5_000_000:
            raise RuntimeError("query planner exceeded split guard")
        block = blocks.pop()
        over_values = [code for code, vals in block.items() if len(vals) > MAX_VALUES]
        if _cell_count(block) <= MAX_CELLS and not over_values:
            ready.append(block)
            continue
        split_code = max(over_values or block, key=lambda code: len(block[code]))
        values = block[split_code]
        if len(values) <= 1:
            candidates = [code for code, vals in block.items() if code != split_code and len(vals) > 1]
            if not candidates:
                ready.append(block)
                continue
            split_code = max(candidates, key=lambda code: len(block[code]))
            values = block[split_code]
        mid = len(values) // 2
        left = dict(block)
        right = dict(block)
        left[split_code] = values[:mid]
        right[split_code] = values[mid:]
        blocks.append(left)
        blocks.append(right)
    return ready


def _category_codes(category: dict) -> list[str]:
    index = category["index"]
    if isinstance(index, dict):
        out = [None] * len(index)
        for code, pos in index.items():
            out[pos] = code
        return out
    return list(index)


def _numeric(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", ""))
        except ValueError:
            return None
    return None


def _iter_rows(doc: dict, colmap: dict[str, str], entity: str):
    order = doc["id"]
    sizes = doc["size"]
    dims = doc["dimension"]
    values = doc.get("value", [])
    time_codes = set(doc.get("role", {}).get("time", []) or [])

    pos_to_code = {}
    code_to_label = {}
    for code in order:
        category = dims[code]["category"]
        pos_to_code[code] = _category_codes(category)
        code_to_label[code] = category.get("label", {})

    strides = [1] * len(order)
    for i in range(len(order) - 2, -1, -1):
        strides[i] = strides[i + 1] * sizes[i + 1]

    for flat, raw_value in enumerate(values):
        obs_value = _numeric(raw_value)
        if obs_value is None:
            continue
        row = {
            "_table_id": ENTITY_PATHS[entity][-1],
            "_table_name": ENTITY_NAMES[entity],
            "_source_updated": ENTITY_UPDATED.get(entity),
            "obs_value": obs_value,
            "obs_time": None,
        }
        for i, code in enumerate(order):
            pos = (flat // strides[i]) % sizes[i]
            category_code = pos_to_code[code][pos]
            label = code_to_label[code].get(category_code, category_code)
            row[colmap[code]] = label
            if code in time_codes:
                row["obs_time"] = label
        yield row


def fetch_one(node_id: str) -> None:
    prefix = f"{SLUG}-"
    entity = node_id[len(prefix):] if node_id.startswith(prefix) else node_id
    url = _url_for(entity)
    meta = _get_json(url)
    variables = meta["variables"]
    used = set()
    colmap = {var["code"]: _sanitize(var["text"], used) for var in variables}
    resolved = _resolve_values(url, variables)
    blocks = _plan_blocks(resolved)

    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        for block in blocks:
            query = {
                "query": [
                    {"code": code, "selection": {"filter": "item", "values": values}}
                    for code, values in block.items()
                ],
                "response": {"format": "json-stat2"},
            }
            doc = _post_json(url, query)
            for row in _iter_rows(doc, colmap, entity):
                fh.write(json.dumps(row, ensure_ascii=False))
                fh.write("\n")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for entity in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Full PX-Web table refresh; skip committed raw assets younger than "
            "7 days to match the connector maintenance cadence."
        ),
        check=lambda asset_id: raw_asset_exists(
            asset_id,
            "ndjson.gz",
            max_age_days=MAINTAIN_MAX_AGE_DAYS,
        ),
    )
    for spec in DOWNLOAD_SPECS
]
