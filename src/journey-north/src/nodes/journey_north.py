"""Journey North sightings — citizen-science point observations behind the
public migration maps (monarchs, milkweed, hummingbirds, robins, orioles,
loons, tulips, ice-out, ...).

Mechanism: the `sightings_json.php` endpoint. One GET per (map_slug, year) with
month=01&day=01&range=365 returns a full calendar year of point sightings for
one map layer in a single response — no pagination, no auth.

Shape: stateless full re-pull. The source exposes no incremental filter
(no since/modifiedAfter/cursor), so each refresh re-fetches every (map_slug,
year) from START_YEAR through the current calendar year. The corpus is small
(~30k sightings/year, a few hundred thousand rows total) but spans ~34 maps ×
~30 years, so each non-empty (map, year) is written as its own raw parquet batch
`journey-north-sightings-{map}-{year}`; the SQL transform glob-unions every
batch (`journey-north-sightings-*`). Historical years are immutable; re-pulling
them each run is cheap (~1100 small requests, a few minutes) and avoids any
stored-watermark drift.
"""

from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import MAP_SLUGS, START_YEAR

BASE = "https://maps.journeynorth.org/sightings_json.php"

# Explicit raw schema — the contract for every (map, year) batch. The endpoint's
# feature shape was reverse-engineered by probing; it is stable.
SCHEMA = pa.schema([
    ("sighting_id", pa.string()),
    ("map_slug", pa.string()),
    ("year", pa.int64()),
    ("season", pa.string()),
    ("date", pa.string()),            # MM/DD/YYYY as delivered; cast in transform
    ("observed_unix", pa.int64()),    # unix epoch seconds
    ("longitude", pa.float64()),
    ("latitude", pa.float64()),
    ("elevation", pa.float64()),
    ("interval", pa.int64()),
    ("pin_id", pa.int64()),
    ("duration", pa.string()),
    ("image_url", pa.string()),
])


@transient_retry()
def _fetch_map_year(map_slug: str, year: int) -> dict:
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
    return resp.json()


def _features(payload: dict):
    """Pull (features, season) out of the `map` envelope."""
    for obj in payload.get("map", []):
        if obj.get("type") == "FeatureCollection":
            return obj.get("features", []), obj.get("season", "")
    return [], ""


def _to_float(v):
    return float(v) if v is not None else None


def _rows(features, map_slug: str, year: int, season: str):
    rows = []
    for feat in features:
        props = feat.get("properties", {})
        geom = feat.get("geometry", {})
        coords = geom.get("coordinates") or []
        sid = props.get("sighting_id")
        rows.append({
            "sighting_id": str(sid) if sid is not None else None,
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


def fetch_sightings(node_id: str) -> None:
    current_year = datetime.now(tz=timezone.utc).year
    for year in range(START_YEAR, current_year + 1):
        for map_slug in MAP_SLUGS:
            payload = _fetch_map_year(map_slug, year)
            features, season = _features(payload)
            if not features:
                continue  # map had no sightings that year — nothing to write
            table = pa.Table.from_pylist(
                _rows(features, map_slug, year, season), schema=SCHEMA
            )
            save_raw_parquet(table, f"{node_id}-{map_slug}-{year}")


DOWNLOAD_SPECS = [
    NodeSpec(id="journey-north-sightings", fn=fetch_sightings, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="journey-north-sightings-transform",
        deps=["journey-north-sightings"],
        sql='''
            WITH ranked AS (
                SELECT
                    sighting_id,
                    map_slug,
                    CAST(year AS INTEGER)                AS year,
                    season,
                    strptime(date, '%m/%d/%Y')::DATE     AS date,
                    to_timestamp(observed_unix)          AS observed_at,
                    CAST(latitude AS DOUBLE)             AS latitude,
                    CAST(longitude AS DOUBLE)            AS longitude,
                    CAST(elevation AS DOUBLE)            AS elevation,
                    CAST(interval AS INTEGER)            AS interval,
                    CAST(pin_id AS INTEGER)              AS pin_id,
                    duration,
                    image_url,
                    row_number() OVER (
                        PARTITION BY map_slug, sighting_id
                        ORDER BY observed_unix
                    ) AS rn
                FROM "journey-north-sightings"
                WHERE sighting_id IS NOT NULL
            )
            SELECT * EXCLUDE (rn)
            FROM ranked
            WHERE rn = 1
        ''',
    ),
]
