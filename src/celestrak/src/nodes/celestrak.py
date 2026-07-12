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
