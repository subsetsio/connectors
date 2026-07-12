"""Journey North data behind the public migration maps.

Sightings are citizen-science point observations behind the public migration
maps. The map taxonomy is the small reference table of map layers.

Mechanism: the `sightings_json.php` endpoint. One GET per (map_slug, year) with
month=01&day=01&range=365 returns a full calendar year of point sightings for
one map layer in a single response: no pagination, no auth.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import pyarrow as pa

from constants import MAP_SLUGS, START_YEAR
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet

BASE = "https://maps.journeynorth.org/sightings_json.php"

SIGHTINGS_SCHEMA = pa.schema([
    ("sighting_id", pa.string()),
    ("map_slug", pa.string()),
    ("year", pa.int64()),
    ("season", pa.string()),
    ("date", pa.string()),
    ("observed_unix", pa.int64()),
    ("longitude", pa.float64()),
    ("latitude", pa.float64()),
    ("elevation", pa.float64()),
    ("interval", pa.int64()),
    ("pin_id", pa.int64()),
    ("duration", pa.string()),
    ("image_url", pa.string()),
])

MAPS_SCHEMA = pa.schema([
    ("map_slug", pa.string()),
    ("display_name", pa.string()),
    ("season", pa.string()),
    ("topic", pa.string()),
    ("event", pa.string()),
    ("is_practice", pa.bool_()),
])


def _fetch_map_year(map_slug: str, year: int) -> tuple[str, int, dict]:
    resp = get(
        BASE,
        params={
            "map": map_slug,
            "year": str(year),
            "month": "01",
            "day": "01",
            "range": "365",
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return map_slug, year, resp.json()


def _features(payload: dict):
    for obj in payload.get("map", []):
        if obj.get("type") == "FeatureCollection":
            return obj.get("features", []), obj.get("season", "")
    return [], ""


def _to_float(value):
    return float(value) if value is not None else None


def _rows(features, map_slug: str, year: int, season: str):
    rows = []
    for feat in features:
        props = feat.get("properties", {})
        geom = feat.get("geometry", {})
        coords = geom.get("coordinates") or []
        sighting_id = props.get("sighting_id")
        rows.append({
            "sighting_id": str(sighting_id) if sighting_id is not None else None,
            "map_slug": map_slug,
            "year": year,
            "season": season or None,
            "date": props.get("date"),
            "observed_unix": props.get("time"),
            "longitude": _to_float(coords[0]) if len(coords) > 0 else None,
            "latitude": _to_float(coords[1]) if len(coords) > 1 else None,
            "elevation": _to_float(coords[2]) if len(coords) > 2 else None,
            "interval": props.get("interval"),
            "pin_id": props.get("pinId"),
            "duration": props.get("duration"),
            "image_url": props.get("imageUrl"),
        })
    return rows


def _season_from_slug(map_slug: str) -> str | None:
    if map_slug.endswith("-spring") or map_slug in {
        "milkweed",
        "signs-spring-other",
        "tulips-spring",
    }:
        return "spring"
    if map_slug.endswith("-fall") or map_slug in {"robin-fall", "signs-fall"}:
        return "fall"
    if map_slug.endswith("-first") or "-first-" in map_slug:
        return "first"
    return None


def _map_row(map_slug: str) -> dict:
    parts = map_slug.split("-")
    season = _season_from_slug(map_slug)
    topic_parts = [
        part
        for part in parts
        if part not in {"any", "fall", "first", "other", "spring"}
    ]
    event_parts = [
        part
        for part in parts
        if part in {"any", "fall", "first", "other", "spring"}
    ]
    return {
        "map_slug": map_slug,
        "display_name": map_slug.replace("-", " ").title(),
        "season": season,
        "topic": " ".join(topic_parts) if topic_parts else map_slug,
        "event": " ".join(event_parts) if event_parts else None,
        "is_practice": map_slug.startswith("practice-"),
    }


def fetch_maps(node_id: str) -> None:
    table = pa.Table.from_pylist([_map_row(slug) for slug in MAP_SLUGS], schema=MAPS_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_sightings(node_id: str) -> None:
    current_year = datetime.now(tz=timezone.utc).year
    jobs = [
        (map_slug, year)
        for year in range(START_YEAR, current_year + 1)
        for map_slug in MAP_SLUGS
    ]
    rows = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(_fetch_map_year, map_slug, year) for map_slug, year in jobs]
        for future in as_completed(futures):
            map_slug, year, payload = future.result()
            features, season = _features(payload)
            if features:
                rows.extend(_rows(features, map_slug, year, season))

    table = pa.Table.from_pylist(rows, schema=SIGHTINGS_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="journey-north-maps", fn=fetch_maps, kind="download"),
    NodeSpec(id="journey-north-sightings", fn=fetch_sightings, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="journey-north-maps-transform",
        deps=["journey-north-maps"],
        key=("map_slug",),
        sql="""
            SELECT
                map_slug,
                display_name,
                season,
                topic,
                event,
                is_practice
            FROM "journey-north-maps"
        """,
    ),
    SqlNodeSpec(
        id="journey-north-sightings-transform",
        deps=["journey-north-sightings"],
        key=("map_slug", "sighting_id"),
        temporal="date",
        sql="""
            WITH ranked AS (
                SELECT
                    sighting_id,
                    map_slug,
                    CAST(year AS INTEGER) AS year,
                    season,
                    strptime(date, '%m/%d/%Y')::DATE AS date,
                    make_timestamp(CAST(observed_unix AS BIGINT) * 1000000) AS observed_at,
                    CAST(latitude AS DOUBLE) AS latitude,
                    CAST(longitude AS DOUBLE) AS longitude,
                    CAST(elevation AS DOUBLE) AS elevation,
                    CAST(interval AS INTEGER) AS interval,
                    CAST(pin_id AS INTEGER) AS pin_id,
                    duration,
                    image_url,
                    row_number() OVER (
                        PARTITION BY map_slug, sighting_id
                        ORDER BY observed_unix DESC
                    ) AS rn
                FROM "journey-north-sightings"
                WHERE sighting_id IS NOT NULL
            )
            SELECT * EXCLUDE (rn)
            FROM ranked
            WHERE rn = 1
        """,
    ),
]
