"""Global Mangrove Watch — Mangrove Atlas REST API connector.

The Mangrove Atlas API (https://mangrove-atlas-api.herokuapp.com/api/v2, the
host the live globalmangrovewatch.org platform calls) exposes per-location
mangrove statistics through ~17 `/widgets/<name>?location_id=<numeric id>`
endpoints plus a `/locations` catalog. Each widget yields a fixed-schema series
across locations, so each widget is published as one long-format Delta table
with the location as a column value.

Scope: we fetch the 122 countries + the worldwide aggregate (national-level
authoritative statistics). The /locations catalog enumerates all 3124 locations
(countries + 3001 WDPA protected areas + worldwide) as a reference table.
Per-protected-area widget series are intentionally out of scope (would 25x the
request fan-out for sparse, GIS-drill-down granularity).

Stateless full re-pull: GMW publishes new annual epochs ~yearly, the corpus is
small (~17 widgets x 123 locations), so every run re-fetches in full and
overwrites. No watermark/cursor. The worldwide location must be queried with NO
location_id param (passing its numeric id 4688 returns empty); countries use
their integer `id`.
"""
import json

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)
from constants import SLUG, WIDGET_IDS

BASE = "https://mangrove-atlas-api.herokuapp.com/api/v2"


def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# spec id -> API widget route (== collect entity id)
ROUTE_BY_ID = {_spec_id(e): e for e in WIDGET_IDS}


@transient_retry()
def _get_json(url: str, params: dict | None = None):
    resp = get(url, params=params or None, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _locations() -> list[dict]:
    data = _get_json(f"{BASE}/locations").get("data", [])
    if not isinstance(data, list) or not data:
        raise AssertionError("locations endpoint returned no data")
    return data


def _flatten(element: dict, base: dict) -> dict:
    rec = dict(base)
    for k, v in element.items():
        rec[k] = json.dumps(v) if isinstance(v, (dict, list)) else v
    return rec


def fetch_widget(node_id: str) -> None:
    """Fetch one widget across all countries + worldwide, emit long-format rows.

    Each (widget, location) response is a {data:[...]|{...}, metadata} envelope.
    We flatten each `data` element (or the single dict) into one ndjson row,
    prefixed with the location identity. Nested values are JSON-encoded so the
    raw stays flat for the SQL transform. A location that errors persistently
    (some widget/country combos 500) is skipped, not fatal.
    """
    route = ROUTE_BY_ID[node_id]
    targets = [
        loc
        for loc in _locations()
        if loc.get("location_type") in ("country", "worldwide")
    ]

    out: list[dict] = []
    skipped = 0
    for loc in targets:
        is_ww = loc.get("location_type") == "worldwide"
        params = None if is_ww else {"location_id": loc.get("id")}
        try:
            payload = _get_json(f"{BASE}/widgets/{route}", params)
        except Exception as exc:  # per-location isolation; log + skip
            skipped += 1
            print(f"[{node_id}] skip location id={loc.get('id')} "
                  f"({loc.get('name')}): {type(exc).__name__}: {exc}")
            continue

        data = payload.get("data")
        if isinstance(data, dict):
            elements = [data]
        elif isinstance(data, list):
            elements = data
        else:
            elements = []

        base = {
            "location_id": loc.get("id"),
            "iso": loc.get("iso"),
            "location_type": loc.get("location_type"),
            "location_name": loc.get("name"),
        }
        for el in elements:
            if isinstance(el, dict):
                out.append(_flatten(el, base))

    print(f"[{node_id}] {len(out)} rows from {len(targets)} locations "
          f"({skipped} skipped)")
    save_raw_ndjson(out, node_id)


def fetch_locations(node_id: str) -> None:
    """Fetch the full location catalog (all 3124: countries, WDPA, worldwide)."""
    rows = []
    for loc in _locations():
        rows.append({
            "id": loc.get("id"),
            "location_uuid": loc.get("location_id"),
            "iso": loc.get("iso"),
            "location_type": loc.get("location_type"),
            "name": loc.get("name"),
            "area_m2": loc.get("area_m2"),
            "coast_length_m": loc.get("coast_length_m"),
            "perimeter_m": loc.get("perimeter_m"),
        })
    print(f"[{node_id}] {len(rows)} locations")
    save_raw_ndjson(rows, node_id)


def fetch_species(node_id: str) -> None:
    """Fetch the mangrove species reference list."""
    data = _get_json(f"{BASE}/species").get("data", [])
    if not isinstance(data, list) or not data:
        raise AssertionError("species endpoint returned no data")

    rows = []
    for species in data:
        rows.append({
            "scientific_name": species.get("scientific_name"),
            "common_name": species.get("common_name"),
            "red_list_cat": species.get("red_list_cat"),
            "iucn_url": species.get("iucn_url"),
            "location_ids": json.dumps(species.get("location_ids") or []),
        })
    print(f"[{node_id}] {len(rows)} species")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id("locations"), fn=fetch_locations, kind="download"),
    NodeSpec(id=_spec_id("species"), fn=fetch_species, kind="download"),
] + [
    NodeSpec(id=_spec_id(eid), fn=fetch_widget, kind="download")
    for eid in WIDGET_IDS
]
