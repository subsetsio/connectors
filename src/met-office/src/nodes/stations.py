"""Met Office historic station data — stations subset.

Per-station reference metadata parsed from file headers. The whole corpus is a
few MB across ~37 tiny files, so this node does a stateless full re-pull every
run (no watermark/cursor).
"""
import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import ROW_RE, STATION_BASE, discover_station_slugs, fetch_text


def _parse_station_meta(slug: str, text: str) -> dict:
    lines = [ln.rstrip("\n") for ln in text.splitlines()]
    name = lines[0].strip() if lines else slug.title()
    # Location info may span the first 1-3 lines (relocations); join them.
    loc_block = " ".join(
        ln.strip()
        for ln in lines[:4]
        if "location" in ln.lower() or re.search(r"\bLat\b", ln) or re.search(r"amsl", ln, re.I)
    )
    lat = re.search(r"Lat\s+(-?\d+(?:\.\d+)?)", loc_block)
    lon = re.search(r"Lon\s+(-?\d+(?:\.\d+)?)", loc_block)
    alt = re.search(r"(-?\d+)\s*m(?:etre|eter)?s?\s*amsl", loc_block, re.IGNORECASE)
    years = [int(m.group(1)) for m in (ROW_RE.match(ln) for ln in lines) if m]
    return {
        "station": slug,
        "name": name or slug.title(),
        "lat": float(lat.group(1)) if lat else None,
        "lon": float(lon.group(1)) if lon else None,
        "altitude_m": int(alt.group(1)) if alt else None,
        "start_year": min(years) if years else None,
        "end_year": max(years) if years else None,
        "location": loc_block or None,
    }


STATION_SCHEMA = pa.schema(
    [
        ("station", pa.string()),
        ("name", pa.string()),
        ("lat", pa.float64()),
        ("lon", pa.float64()),
        ("altitude_m", pa.int64()),
        ("start_year", pa.int64()),
        ("end_year", pa.int64()),
        ("location", pa.string()),
    ]
)


def fetch_stations(node_id: str) -> None:
    asset = node_id
    rows = []
    for slug in discover_station_slugs():
        text = fetch_text(f"{STATION_BASE}/{slug}data.txt")
        rows.append(_parse_station_meta(slug, text))
    if not rows:
        raise AssertionError("parsed 0 station metadata records")
    table = pa.Table.from_pylist(rows, schema=STATION_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="met-office-stations", fn=fetch_stations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="met-office-stations-transform",
        deps=["met-office-stations"],
        sql='''
            SELECT
                station,
                name,
                lat,
                lon,
                CAST(altitude_m AS INTEGER) AS altitude_m,
                CAST(start_year AS INTEGER) AS start_year,
                CAST(end_year AS INTEGER)   AS end_year,
                location
            FROM "met-office-stations"
        ''',
    ),
]
