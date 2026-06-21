"""CelesTrak connector — Satellite Catalog (SATCAT) and derived statistics.

Single upstream source: the full SATCAT CSV at https://celestrak.org/pub/satcat.csv
(~69k rows, one per cataloged space object since 1957, no auth, persistent URL,
updated multiple times daily). There is no incremental query parameter, so each
refresh re-pulls the whole corpus (a single ~10MB GET — cheap) and overwrites.

Three published subsets, all derived from that one download via DuckDB:
  - satellite-catalog    : the cleaned object-level catalog (reference).
  - launches-by-country  : annual object counts by owner country & type.
  - constellation-growth : annual cumulative counts for major constellations.

Each subset is a separate collect entity, so each gets its own DOWNLOAD_SPEC
(the harness requires one download per entity, each consumed by a transform).
The three downloads fetch the same SATCAT and each save it under their own raw
asset id; their transforms then read that raw view. The redundant fetch is the
price of the one-download-per-entity contract and is negligible at this size.
"""
import csv
from io import StringIO

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
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


@transient_retry()
def _fetch_satcat_text() -> str:
    resp = get(SATCAT_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


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
    """Fetch the full SATCAT CSV and save it as parquet under this node's asset id.

    Shared by all three download specs — each writes its own raw copy so its
    transform has a dep view to read. Stateless full re-pull every run.
    """
    asset = node_id
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
        raise AssertionError(f"{asset}: SATCAT returned 0 rows — source format may have changed")

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="celestrak-satellite-catalog", fn=fetch_satcat, kind="download"),
    NodeSpec(id="celestrak-launches-by-country", fn=fetch_satcat, kind="download"),
    NodeSpec(id="celestrak-constellation-growth", fn=fetch_satcat, kind="download"),
]


# --- Transforms -----------------------------------------------------------

# Object-name prefix -> (constellation, category) for constellation-growth.
_CONSTELLATIONS = [
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


def _case(value_idx: int) -> str:
    """Build a DuckDB CASE mapping object_name prefixes to constellation
    (value_idx=0) or category (value_idx=1)."""
    whens = [
        f"WHEN UPPER(object_name) LIKE '{row[0]}%' THEN '{row[value_idx + 1]}'"
        for row in _CONSTELLATIONS
    ]
    return "CASE " + " ".join(whens) + " ELSE NULL END"


_CONSTELLATION_CASE = _case(0)
_CATEGORY_CASE = _case(1)


_SATELLITE_CATALOG_SQL = """
    SELECT
        norad_cat_id AS norad_id,
        object_id,
        object_name AS name,
        CASE object_type
            WHEN 'PAY' THEN 'PAYLOAD'
            WHEN 'R/B' THEN 'ROCKET_BODY'
            WHEN 'DEB' THEN 'DEBRIS'
            ELSE 'UNKNOWN'
        END AS object_type,
        CASE ops_status_code
            WHEN '+' THEN 'ACTIVE'
            WHEN '-' THEN 'INACTIVE'
            WHEN 'P' THEN 'PARTIALLY_OPERATIONAL'
            WHEN 'B' THEN 'BACKUP'
            WHEN 'S' THEN 'STANDBY'
            WHEN 'X' THEN 'EXTENDED'
            WHEN 'D' THEN 'DECAYED'
            ELSE 'UNKNOWN'
        END AS status,
        owner,
        launch_date,
        launch_site,
        decay_date,
        period AS period_minutes,
        inclination AS inclination_degrees,
        apogee AS apogee_km,
        perigee AS perigee_km
    FROM "celestrak-satellite-catalog"
    WHERE norad_cat_id IS NOT NULL
"""


_LAUNCHES_BY_COUNTRY_SQL = """
    SELECT
        SUBSTRING(launch_date, 1, 4) AS year,
        COALESCE(owner, 'UNKNOWN') AS country,
        SUM(CASE WHEN object_type = 'PAY' THEN 1 ELSE 0 END)::BIGINT AS payloads,
        SUM(CASE WHEN object_type = 'R/B' THEN 1 ELSE 0 END)::BIGINT AS rocket_bodies,
        SUM(CASE WHEN object_type = 'DEB' THEN 1 ELSE 0 END)::BIGINT AS debris,
        COUNT(*)::BIGINT AS total
    FROM "celestrak-launches-by-country"
    WHERE launch_date IS NOT NULL AND launch_date != ''
    GROUP BY year, country
    ORDER BY year, country
"""


_CONSTELLATION_GROWTH_SQL = f"""
    WITH satellites AS (
        SELECT
            SUBSTRING(launch_date, 1, 4) AS year,
            {_CONSTELLATION_CASE} AS constellation,
            {_CATEGORY_CASE} AS category,
            ops_status_code
        FROM "celestrak-constellation-growth"
        WHERE object_type = 'PAY'
            AND launch_date IS NOT NULL
            AND launch_date != ''
    ),
    yearly AS (
        SELECT
            constellation,
            category,
            year,
            COUNT(*)::BIGINT AS launched_that_year,
            SUM(CASE WHEN ops_status_code != 'D' THEN 1 ELSE 0 END)::BIGINT AS active_in_year
        FROM satellites
        WHERE constellation IS NOT NULL
        GROUP BY constellation, category, year
    )
    SELECT
        year,
        constellation,
        category,
        launched_that_year,
        SUM(launched_that_year) OVER (PARTITION BY constellation ORDER BY year)::BIGINT AS cumulative_total,
        SUM(active_in_year) OVER (PARTITION BY constellation)::BIGINT AS active_count
    FROM yearly
    ORDER BY constellation, year
"""


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="celestrak-satellite-catalog-transform",
        deps=["celestrak-satellite-catalog"],
        sql=_SATELLITE_CATALOG_SQL,
    ),
    SqlNodeSpec(
        id="celestrak-launches-by-country-transform",
        deps=["celestrak-launches-by-country"],
        sql=_LAUNCHES_BY_COUNTRY_SQL,
    ),
    SqlNodeSpec(
        id="celestrak-constellation-growth-transform",
        deps=["celestrak-constellation-growth"],
        sql=_CONSTELLATION_GROWTH_SQL,
    ),
]
