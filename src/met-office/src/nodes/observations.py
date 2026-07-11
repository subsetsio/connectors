"""Met Office historic station data — observations subset.

Long-format monthly rows (station x year x month). The whole corpus is a few MB
across ~37 tiny files, so this node does a stateless full re-pull every run (no
watermark/cursor) — revisions and the rolling-monthly 'Provisional' tail are
picked up for free.
"""
import re

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import ROW_RE, STATION_BASE, discover_station_slugs, fetch_text

_NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


def _clean_value(tok: str):
    """Strip estimate (*) / sensor (#) markers, map missing (---) to None, and
    take the leading numeric value (some cells glue an inline annotation, e.g.
    '152.0Change')."""
    t = tok.replace("*", "").replace("#", "").strip()
    if not t or set(t) <= {"-"}:
        return None
    m = _NUM_RE.match(t)
    return m.group(0) if m else None


def _parse_observations(slug: str, text: str) -> list:
    """One dict per monthly row for a single station."""
    lines = text.splitlines()
    rows = []
    for line in lines:
        m = ROW_RE.match(line)
        if not m:
            continue  # header, units, legend, 'Site closed', blanks
        year = int(m.group(1))
        month = int(m.group(2))
        if not (1 <= month <= 12):
            continue
        rest = m.group(3)
        provisional = "provisional" in rest.lower()
        toks = rest.split()
        vals = [t for t in toks if t.lower() != "provisional"]
        if len(vals) < 5:
            continue  # malformed / truncated row
        tmax, tmin, af, rain, sun = (_clean_value(v) for v in vals[:5])
        rows.append(
            {
                "station": slug,
                "year": year,
                "month": month,
                "tmax_degc": float(tmax) if tmax is not None else None,
                "tmin_degc": float(tmin) if tmin is not None else None,
                "af_days": int(round(float(af))) if af is not None else None,
                "rain_mm": float(rain) if rain is not None else None,
                "sun_hours": float(sun) if sun is not None else None,
                "provisional": provisional,
            }
        )
    return rows


OBS_SCHEMA = pa.schema(
    [
        ("station", pa.string()),
        ("year", pa.int64()),
        ("month", pa.int64()),
        ("tmax_degc", pa.float64()),
        ("tmin_degc", pa.float64()),
        ("af_days", pa.int64()),
        ("rain_mm", pa.float64()),
        ("sun_hours", pa.float64()),
        ("provisional", pa.bool_()),
    ]
)


def fetch_observations(node_id: str) -> None:
    asset = node_id
    rows = []
    for slug in discover_station_slugs():
        text = fetch_text(f"{STATION_BASE}/{slug}data.txt")
        rows.extend(_parse_observations(slug, text))
    if not rows:
        raise AssertionError("parsed 0 observation rows across all stations")
    table = pa.Table.from_pylist(rows, schema=OBS_SCHEMA)
    save_raw_parquet(table, asset)
