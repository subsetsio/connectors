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
    SqlNodeSpec,
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


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id("locations"), fn=fetch_locations, kind="download"),
] + [
    NodeSpec(id=_spec_id(eid), fn=fetch_widget, kind="download")
    for eid in WIDGET_IDS
]


# --- Transforms: one published Delta table per subset --------------------
# Shared leading location columns for every widget table.
_LOC = 'CAST(location_id AS BIGINT) AS location_id, iso, location_type, location_name'

_TRANSFORM_SQL = {
    "locations": f'''
        SELECT
            CAST(id AS BIGINT)              AS location_id,
            location_uuid,
            iso,
            location_type,
            name                           AS location_name,
            TRY_CAST(area_m2 AS DOUBLE)        AS area_m2,
            TRY_CAST(coast_length_m AS DOUBLE) AS coast_length_m,
            TRY_CAST(perimeter_m AS DOUBLE)    AS perimeter_m
        FROM "{_spec_id("locations")}"
    ''',
    "habitat_extent": f'''
        SELECT {_LOC},
            CAST(year AS INTEGER) AS year,
            indicator,
            CAST(value AS DOUBLE) AS value
        FROM "{_spec_id("habitat_extent")}"
        WHERE value IS NOT NULL
    ''',
    "net_change": f'''
        SELECT {_LOC},
            CAST(year AS INTEGER)      AS year,
            CAST(net_change AS DOUBLE) AS net_change,
            TRY_CAST(gain AS DOUBLE)   AS gain,
            TRY_CAST(loss AS DOUBLE)   AS loss
        FROM "{_spec_id("net_change")}"
        WHERE net_change IS NOT NULL
    ''',
    "aboveground_biomass": f'''
        SELECT {_LOC},
            CAST(year AS INTEGER) AS year,
            indicator,
            CAST(value AS DOUBLE) AS value
        FROM "{_spec_id("aboveground_biomass")}"
        WHERE value IS NOT NULL
    ''',
    "blue_carbon": f'''
        SELECT {_LOC},
            CAST(year AS INTEGER) AS year,
            indicator,
            CAST(value AS DOUBLE) AS value
        FROM "{_spec_id("blue_carbon")}"
        WHERE value IS NOT NULL
    ''',
    "tree_height": f'''
        SELECT {_LOC},
            CAST(year AS INTEGER) AS year,
            indicator,
            CAST(value AS DOUBLE) AS value
        FROM "{_spec_id("tree_height")}"
        WHERE value IS NOT NULL
    ''',
    "degradation-and-loss": f'''
        SELECT {_LOC},
            indicator,
            label,
            CAST(value AS DOUBLE) AS value
        FROM "{_spec_id("degradation-and-loss")}"
        WHERE value IS NOT NULL
    ''',
    "restoration-potential": f'''
        SELECT {_LOC},
            TRY_CAST(restoration_potential_score AS DOUBLE) AS restoration_potential_score,
            TRY_CAST(restorable_area AS DOUBLE)             AS restorable_area,
            TRY_CAST(restorable_area_perc AS DOUBLE)        AS restorable_area_perc,
            TRY_CAST(mangrove_area_extent AS DOUBLE)        AS mangrove_area_extent
        FROM "{_spec_id("restoration-potential")}"
    ''',
    "mitigation_potentials": f'''
        SELECT {_LOC},
            TRY_CAST(year AS INTEGER) AS year,
            indicator,
            category,
            CAST(value AS DOUBLE) AS value
        FROM "{_spec_id("mitigation_potentials")}"
        WHERE value IS NOT NULL
    ''',
    "protected-areas": f'''
        SELECT {_LOC},
            CAST(year AS INTEGER)          AS year,
            CAST(total_area AS DOUBLE)     AS total_area,
            CAST(protected_area AS DOUBLE) AS protected_area
        FROM "{_spec_id("protected-areas")}"
    ''',
    "ecosystem_services": f'''
        SELECT {_LOC},
            indicator,
            CAST(value AS DOUBLE) AS value
        FROM "{_spec_id("ecosystem_services")}"
        WHERE value IS NOT NULL
    ''',
    "biodiversity": f'''
        SELECT {_LOC},
            CAST(total AS INTEGER)      AS total_species,
            CAST(threatened AS INTEGER) AS threatened_species,
            categories                  AS categories_json
        FROM "{_spec_id("biodiversity")}"
    ''',
    "blue-carbon-investment": f'''
        SELECT {_LOC},
            category,
            label,
            CAST(value AS DOUBLE)      AS value,
            CAST(percentage AS DOUBLE) AS percentage
        FROM "{_spec_id("blue-carbon-investment")}"
        WHERE value IS NOT NULL
    ''',
    "drivers_of_change": f'''
        SELECT {_LOC},
            variable,
            primary_driver,
            CAST(value AS DOUBLE) AS value
        FROM "{_spec_id("drivers_of_change")}"
        WHERE value IS NOT NULL
    ''',
    "ecoregions": f'''
        SELECT {_LOC},
            indicator,
            category,
            CAST(value AS DOUBLE) AS value
        FROM "{_spec_id("ecoregions")}"
        WHERE value IS NOT NULL
    ''',
    "fisheries": f'''
        SELECT {_LOC},
            indicator,
            category,
            TRY_CAST(year AS INTEGER) AS year,
            CAST(value AS DOUBLE)     AS value
        FROM "{_spec_id("fisheries")}"
        WHERE value IS NOT NULL
    ''',
    "fishery_mitigation_potentials": f'''
        SELECT {_LOC},
            indicator,
            indicator_type,
            CAST(value AS DOUBLE) AS value
        FROM "{_spec_id("fishery_mitigation_potentials")}"
        WHERE value IS NOT NULL
    ''',
    "international_status": f'''
        SELECT {_LOC},
            * EXCLUDE (location_id, iso, location_type, location_name)
        FROM "{_spec_id("international_status")}"
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=_TRANSFORM_SQL[ROUTE_BY_ID.get(spec.id, "locations")],
    )
    for spec in DOWNLOAD_SPECS
]
