"""CelesTrak connector — Satellite Catalog (SATCAT) and derived statistics.

Single upstream source: the full SATCAT CSV at https://celestrak.org/pub/satcat.csv
(~69k rows, one per cataloged space object since 1957, no auth, persistent URL,
updated multiple times daily). There is no incremental query parameter, so each
refresh re-pulls the whole corpus (a single ~10MB GET — cheap) and overwrites.

Three published subsets, all derived from the SATCAT CSV:
  - satellite-catalog    : the cleaned object-level catalog (reference).
  - launches-by-country  : annual object counts by owner country & type.
  - constellation-growth : annual cumulative counts for major constellations.
"""
import csv
from collections import defaultdict
from io import StringIO

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)


SATCAT_URL = "https://celestrak.org/pub/satcat.csv"

# Raw SATCAT schema — declared explicitly so parquet writes are a stable contract.
# Column names mirror the source CSV header (lowercased). Numeric fields are
# nullable because the source leaves them blank for objects without orbital data.
SCHEMA = pa.schema([
    ("object_name", pa.string()),
    ("object_id", pa.string()),
    ("norad_cat_id", pa.int64()),
    ("object_type", pa.string()),
    ("ops_status_code", pa.string()),
    ("owner", pa.string()),
    ("launch_date", pa.string()),
    ("launch_site", pa.string()),
    ("decay_date", pa.string()),
    ("period", pa.float64()),
    ("inclination", pa.float64()),
    ("apogee", pa.float64()),
    ("perigee", pa.float64()),
    ("rcs", pa.float64()),
    ("data_status_code", pa.string()),
    ("orbit_center", pa.string()),
    ("orbit_type", pa.string()),
])

LAUNCHES_BY_COUNTRY_SCHEMA = pa.schema([
    ("year", pa.string()),
    ("country", pa.string()),
    ("payloads", pa.int64()),
    ("rocket_bodies", pa.int64()),
    ("debris", pa.int64()),
    ("total", pa.int64()),
])

CONSTELLATION_GROWTH_SCHEMA = pa.schema([
    ("year", pa.string()),
    ("constellation", pa.string()),
    ("category", pa.string()),
    ("launched_that_year", pa.int64()),
    ("cumulative_total", pa.int64()),
    ("active_count", pa.int64()),
])


def _fetch_satcat_text() -> str:
    resp = get(SATCAT_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _load_satcat_rows() -> list[dict]:
    text = _fetch_satcat_text()
    reader = csv.DictReader(StringIO(text))

    rows = []
    for r in reader:
        rows.append({
            "object_name": _str(r.get("OBJECT_NAME")),
            "object_id": _str(r.get("OBJECT_ID")),
            "norad_cat_id": _int(r.get("NORAD_CAT_ID")),
            "object_type": _str(r.get("OBJECT_TYPE")),
            "ops_status_code": _str(r.get("OPS_STATUS_CODE")),
            "owner": _str(r.get("OWNER")),
            "launch_date": _str(r.get("LAUNCH_DATE")),
            "launch_site": _str(r.get("LAUNCH_SITE")),
            "decay_date": _str(r.get("DECAY_DATE")),
            "period": _float(r.get("PERIOD")),
            "inclination": _float(r.get("INCLINATION")),
            "apogee": _float(r.get("APOGEE")),
            "perigee": _float(r.get("PERIGEE")),
            "rcs": _float(r.get("RCS")),
            "data_status_code": _str(r.get("DATA_STATUS_CODE")),
            "orbit_center": _str(r.get("ORBIT_CENTER")),
            "orbit_type": _str(r.get("ORBIT_TYPE")),
        })

    if not rows:
        raise AssertionError("SATCAT returned 0 rows — source format may have changed")
    return rows


def _str(v):
    v = (v or "").strip()
    return v or None


def _int(v):
    v = (v or "").strip()
    return int(v) if v else None


def _float(v):
    v = (v or "").strip()
    return float(v) if v else None


def fetch_satcat(node_id: str) -> None:
    """Fetch the full SATCAT CSV and save it as object-level parquet."""
    asset = node_id
    rows = _load_satcat_rows()
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


def _constellation_for(name: str | None) -> tuple[str, str] | tuple[None, None]:
    upper = (name or "").upper()
    rules = [
        ("STARLINK", "Starlink", "communications"),
        ("ONEWEB", "OneWeb", "communications"),
        ("KUIPER", "Kuiper", "communications"),
        ("IRIDIUM", "Iridium", "communications"),
        ("GLOBALSTAR", "Globalstar", "communications"),
        ("ORBCOMM", "Orbcomm", "communications"),
        ("INTELSAT", "Intelsat", "communications"),
        ("EUTELSAT", "Eutelsat", "communications"),
        ("TELESAT", "Telesat", "communications"),
        ("QIANFAN", "Qianfan (G60)", "communications"),
        ("NAVSTAR", "GPS", "navigation"),
        ("GPS", "GPS", "navigation"),
        ("GLONASS", "GLONASS", "navigation"),
        ("GSAT", "Galileo", "navigation"),
        ("GALILEO", "Galileo", "navigation"),
        ("BEIDOU", "BeiDou", "navigation"),
        ("NOAA", "NOAA", "weather"),
        ("GOES", "GOES", "weather"),
        ("METEOSAT", "Meteosat", "weather"),
        ("PLANET", "Planet Labs", "earth_observation"),
        ("DOVE", "Planet Labs", "earth_observation"),
        ("FLOCK", "Planet Labs", "earth_observation"),
        ("SPIRE", "Spire", "earth_observation"),
        ("LEMUR", "Spire", "earth_observation"),
    ]
    for prefix, constellation, category in rules:
        if upper.startswith(prefix):
            return constellation, category
    return None, None


def fetch_launches_by_country(node_id: str) -> None:
    grouped = defaultdict(lambda: {"payloads": 0, "rocket_bodies": 0, "debris": 0, "total": 0})
    for row in _load_satcat_rows():
        launch_date = row["launch_date"]
        if not launch_date:
            continue
        key = (launch_date[:4], row["owner"] or "UNKNOWN")
        grouped[key]["total"] += 1
        if row["object_type"] == "PAY":
            grouped[key]["payloads"] += 1
        elif row["object_type"] == "R/B":
            grouped[key]["rocket_bodies"] += 1
        elif row["object_type"] == "DEB":
            grouped[key]["debris"] += 1

    rows = [
        {
            "year": year,
            "country": country,
            "payloads": counts["payloads"],
            "rocket_bodies": counts["rocket_bodies"],
            "debris": counts["debris"],
            "total": counts["total"],
        }
        for (year, country), counts in sorted(grouped.items())
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=LAUNCHES_BY_COUNTRY_SCHEMA), node_id)


def fetch_constellation_growth(node_id: str) -> None:
    yearly = defaultdict(lambda: {"launched_that_year": 0, "active_in_year": 0})
    for row in _load_satcat_rows():
        if row["object_type"] != "PAY" or not row["launch_date"]:
            continue
        constellation, category = _constellation_for(row["object_name"])
        if constellation is None:
            continue
        key = (constellation, category, row["launch_date"][:4])
        yearly[key]["launched_that_year"] += 1
        if row["ops_status_code"] != "D":
            yearly[key]["active_in_year"] += 1

    active_by_constellation = defaultdict(int)
    for (constellation, _category, _year), counts in yearly.items():
        active_by_constellation[constellation] += counts["active_in_year"]

    cumulative = defaultdict(int)
    rows = []
    for constellation, category, year in sorted(yearly):
        counts = yearly[(constellation, category, year)]
        cumulative[constellation] += counts["launched_that_year"]
        rows.append({
            "year": year,
            "constellation": constellation,
            "category": category,
            "launched_that_year": counts["launched_that_year"],
            "cumulative_total": cumulative[constellation],
            "active_count": active_by_constellation[constellation],
        })

    save_raw_parquet(pa.Table.from_pylist(rows, schema=CONSTELLATION_GROWTH_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="celestrak-satellite-catalog", fn=fetch_satcat, kind="download"),
    NodeSpec(id="celestrak-launches-by-country", fn=fetch_launches_by_country, kind="download"),
    NodeSpec(id="celestrak-constellation-growth", fn=fetch_constellation_growth, kind="download"),
]
