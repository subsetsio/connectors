"""Global Fishing Watch — Global AIS-based Apparent Fishing Effort Dataset (Zenodo).

Mechanism: bulk_zenodo (research-chosen). The dataset is published as a single
versioned Zenodo record (DOI 10.5281/zenodo.14982712) of ZIP-of-CSV files, no auth.

Two published products, each its own raw parquet + SQL transform:
  - fleet-monthly-10 : apparent fishing effort by flag x geartype, 0.1deg grid, monthly
  - fishing-vessels  : per-vessel-year characteristics table

The heavier daily products (mmsi-daily-10, fleet-daily-100) were deferred at the
accept stage on pull-cost grounds and are intentionally not built here.

Fetch shape: stateless full re-pull. The record is a static versioned snapshot with
no incremental/delta query, so every refresh re-fetches the whole corpus and overwrites.
The two time-partitioned products ship one ZIP per calendar year (each ZIP holds one
CSV per period); we stream each year's inner CSVs into a single streamed parquet to keep
memory bounded regardless of year size. A new dataset version would arrive as a new
Zenodo record/DOI (bump RECORD_ID).
"""

import io
import re
import zipfile

import pyarrow as pa
from pyarrow import csv as pacsv

from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

RECORD_ID = "14982712"
RECORD_API = f"https://zenodo.org/api/records/{RECORD_ID}"

# --- Product schemas (from the record's machine-readable *.schema.json sidecars) ---

FLEET_MONTHLY_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("cell_ll_lat", pa.float64()),
    ("cell_ll_lon", pa.float64()),
    ("flag", pa.string()),
    ("geartype", pa.string()),
    ("hours", pa.float64()),
    ("fishing_hours", pa.float64()),
    ("mmsi_present", pa.int32()),
])

FISHING_VESSELS_SCHEMA = pa.schema([
    ("mmsi", pa.string()),
    ("year", pa.int32()),
    ("flag_ais", pa.string()),
    ("flag_registry", pa.string()),
    ("flag_gfw", pa.string()),
    ("vessel_class_inferred", pa.string()),
    ("vessel_class_inferred_score", pa.float64()),
    ("vessel_class_registry", pa.string()),
    ("vessel_class_gfw", pa.string()),
    ("self_reported_fishing_vessel", pa.bool_()),
    ("length_m_inferred", pa.float64()),
    ("length_m_registry", pa.float64()),
    ("length_m_gfw", pa.float64()),
    ("engine_power_kw_inferred", pa.float64()),
    ("engine_power_kw_registry", pa.float64()),
    ("engine_power_kw_gfw", pa.float64()),
    ("tonnage_gt_inferred", pa.float64()),
    ("tonnage_gt_registry", pa.float64()),
    ("tonnage_gt_gfw", pa.float64()),
    ("registries_listed", pa.string()),
    ("active_hours", pa.float64()),
    ("fishing_hours", pa.float64()),
])

# Per-entity config. entity_id -> {file_prefix, schema, partitioned}.
# "partitioned" products are per-year ZIPs of per-period CSVs; the single product
# (fishing-vessels) is one flat CSV. file_prefix matches the Zenodo file `key`.
PRODUCTS = {
    "fleet-monthly-10": {
        "file_prefix": "fleet-monthly-csvs-10-v3-",
        "schema": FLEET_MONTHLY_SCHEMA,
        "partitioned": True,
    },
    "fishing-vessels": {
        "file_prefix": "fishing-vessels-v3.csv",
        "schema": FISHING_VESSELS_SCHEMA,
        "partitioned": False,
    },
}

SLUG = "global-fishing-watch"


@transient_retry()
def _record_files() -> list[dict]:
    """List the Zenodo record's files: [{key, size, links.self}, ...]."""
    resp = get(RECORD_API, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()["files"]


@transient_retry(attempts=6, min_wait=4, max_wait=120)
def _download_bytes(url: str) -> bytes:
    """Download a whole file (zip or csv) into memory. Used for one year ZIP or the
    single vessel CSV at a time — bounded by the largest single file (~0.75GB)."""
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _csv_bytes_to_table(data: bytes, schema: pa.Schema) -> pa.Table:
    """Parse one CSV payload into a table conforming exactly to `schema`."""
    table = pacsv.read_csv(
        io.BytesIO(data),
        convert_options=pacsv.ConvertOptions(
            column_types={f.name: f.type for f in schema},
            strings_can_be_null=True,
        ),
    )
    return table.select(schema.names).cast(schema)


def _entity_of(node_id: str) -> str:
    """Recover the collect entity id from the spec id."""
    assert node_id.startswith(SLUG + "-"), f"unexpected node id {node_id!r}"
    return node_id[len(SLUG) + 1:]


def _fetch_partitioned(node_id: str, cfg: dict) -> None:
    """Stream every per-year ZIP of a product into one bounded-memory parquet."""
    schema = cfg["schema"]
    prefix = cfg["file_prefix"]
    files = _record_files()
    year_files = [
        f for f in files
        if f["key"].startswith(prefix) and f["key"].endswith(".zip")
    ]
    if not year_files:
        raise AssertionError(f"{node_id}: no year ZIPs match prefix {prefix!r} on record {RECORD_ID}")
    # Deterministic order by the 4-digit year embedded in the filename.
    def _year(f: dict) -> int:
        m = re.search(r"(\d{4})\.zip$", f["key"])
        if not m:
            raise AssertionError(f"{node_id}: cannot parse year from {f['key']!r}")
        return int(m.group(1))
    year_files.sort(key=_year)

    total_rows = 0
    with raw_parquet_writer(node_id, schema) as writer:
        for f in year_files:
            blob = _download_bytes(f["links"]["self"])
            zf = zipfile.ZipFile(io.BytesIO(blob))
            members = sorted(n for n in zf.namelist() if n.endswith(".csv"))
            if not members:
                raise AssertionError(f"{node_id}: ZIP {f['key']!r} has no CSV members")
            for member in members:
                table = _csv_bytes_to_table(zf.read(member), schema)
                if table.num_rows:
                    writer.write_table(table)
                    total_rows += table.num_rows
            print(f"  {node_id}: {f['key']} -> {len(members)} files, running rows {total_rows:,}")
    if total_rows == 0:
        raise AssertionError(f"{node_id}: wrote 0 rows across {len(year_files)} year ZIPs")


def _fetch_single_csv(node_id: str, cfg: dict) -> None:
    """Fetch the single flat CSV product (fishing-vessels) and write one parquet."""
    schema = cfg["schema"]
    files = _record_files()
    matches = [f for f in files if f["key"] == cfg["file_prefix"]]
    if not matches:
        raise AssertionError(f"{node_id}: file {cfg['file_prefix']!r} not found on record {RECORD_ID}")
    table = _csv_bytes_to_table(_download_bytes(matches[0]["links"]["self"]), schema)
    if table.num_rows == 0:
        raise AssertionError(f"{node_id}: parsed 0 rows from {cfg['file_prefix']!r}")
    save_raw_parquet(table, node_id)


def fetch_one(node_id: str) -> None:
    """Single entry point for every download spec; dispatches by entity config."""
    entity = _entity_of(node_id)
    cfg = PRODUCTS[entity]
    if cfg["partitioned"]:
        _fetch_partitioned(node_id, cfg)
    else:
        _fetch_single_csv(node_id, cfg)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for entity in PRODUCTS
]

# Transforms are NOT authored here — they are compiled from the settled model in
# the model stage (`compile-transforms --write` -> src/transforms/<table>.sql|.yml).
# Module-level TRANSFORM_SPECS is retired.
