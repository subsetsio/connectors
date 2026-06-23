"""Department for Transport (UK) — road-traffic statistics.

Chosen mechanism: roadtraffic_bulk_csv. Each subset is one stable object on the
public Google Cloud Storage bucket `dft-statistics` under the prefix
road-traffic/downloads/data-gov-uk/. Small aggregate datasets are plain CSV;
the large count-point datasets are a single CSV inside a ZIP. There is no
incremental query surface (no since/cursor) and the whole object is rewritten
in place on each annual release, so every node does a stateless full re-pull and
overwrites — revisions are picked up for free.

Raw is written as Parquet (`<id>.parquet`), streamed batch-by-batch straight
from the source CSV (the ~1GB uncompressed raw_counts file never lands fully in
memory). The CSV is parsed with PyArrow rather than handed to DuckDB's CSV
auto-detection because the source encodes nulls as the literal token ``NA`` on
minor-road rows (e.g. ``link_length_km``); PyArrow maps ``NA`` to null while
keeping the column numeric, so the typed Parquet feeds the TRANSFORM_SPECS
cleanly. DuckDB reads the Parquet views in TRANSFORM_SPECS, where each subset is
cast/renamed into its published Delta table.
"""

import io
import zipfile

import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_parquet_writer, transient_retry

BASE = "https://storage.googleapis.com/dft-statistics/road-traffic/downloads/data-gov-uk/"

# spec id -> source filename on the GCS bucket. Plain .csv are written through
# unchanged; .zip hold a single CSV member that is streamed out.
DATASETS = {
    "department-for-transport-dft-traffic-counts-aadf": "dft_traffic_counts_aadf.zip",
    "department-for-transport-dft-traffic-counts-aadf-by-direction": "dft_traffic_counts_aadf_by_direction.zip",
    "department-for-transport-dft-traffic-counts-raw-counts": "dft_traffic_counts_raw_counts.zip",
    "department-for-transport-local-authority-traffic": "local_authority_traffic.csv",
    "department-for-transport-region-traffic-by-road-type": "region_traffic_by_road_type.csv",
    "department-for-transport-region-traffic-by-vehicle-type": "region_traffic_by_vehicle_type.csv",
}

# Block large enough that the first chunk spans many count points / road types,
# so PyArrow's per-column type inference sees real values (not an all-NA prefix).
_READ_OPTS = pacsv.ReadOptions(block_size=64 * 1024 * 1024)
# The source writes "NA" for missing numerics; map it (and bare empties) to null.
_CONVERT_OPTS = pacsv.ConvertOptions(null_values=["NA", ""], strings_can_be_null=True)


@transient_retry()
def _fetch(url: str):
    # Read timeout is generous: raw_counts.zip is ~88MB over a single request.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp


def _csv_to_parquet(fileobj, asset: str) -> None:
    reader = pacsv.open_csv(
        fileobj, read_options=_READ_OPTS, convert_options=_CONVERT_OPTS
    )
    with raw_parquet_writer(asset, reader.schema) as writer:
        for batch in reader:
            writer.write_batch(batch)


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the raw asset name
    filename = DATASETS[node_id]
    resp = _fetch(BASE + filename)

    if filename.endswith(".zip"):
        zf = zipfile.ZipFile(io.BytesIO(resp.content))
        member = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
        with zf.open(member) as src:
            _csv_to_parquet(src, asset)
    else:
        _csv_to_parquet(io.BytesIO(resp.content), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="department-for-transport-dft-traffic-counts-aadf", fn=fetch_one, kind="download"),
    NodeSpec(id="department-for-transport-dft-traffic-counts-aadf-by-direction", fn=fetch_one, kind="download"),
    NodeSpec(id="department-for-transport-dft-traffic-counts-raw-counts", fn=fetch_one, kind="download"),
    NodeSpec(id="department-for-transport-local-authority-traffic", fn=fetch_one, kind="download"),
    NodeSpec(id="department-for-transport-region-traffic-by-road-type", fn=fetch_one, kind="download"),
    NodeSpec(id="department-for-transport-region-traffic-by-vehicle-type", fn=fetch_one, kind="download"),
]


_AADF = "department-for-transport-dft-traffic-counts-aadf"
_AADF_DIR = "department-for-transport-dft-traffic-counts-aadf-by-direction"
_RAW = "department-for-transport-dft-traffic-counts-raw-counts"
_LA = "department-for-transport-local-authority-traffic"
_REGION_ROAD = "department-for-transport-region-traffic-by-road-type"
_REGION_VEH = "department-for-transport-region-traffic-by-vehicle-type"

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_AADF}-transform",
        deps=[_AADF],
        sql=f'''
            SELECT
                CAST(count_point_id AS BIGINT)        AS count_point_id,
                CAST(year AS INTEGER)                 AS year,
                CAST(region_id AS INTEGER)            AS region_id,
                region_name,
                region_ons_code,
                CAST(local_authority_id AS INTEGER)   AS local_authority_id,
                local_authority_name,
                local_authority_code,
                road_name,
                road_category,
                road_type,
                CAST(easting AS BIGINT)               AS easting,
                CAST(northing AS BIGINT)              AS northing,
                CAST(latitude AS DOUBLE)              AS latitude,
                CAST(longitude AS DOUBLE)             AS longitude,
                CAST(link_length_km AS DOUBLE)        AS link_length_km,
                CAST(link_length_miles AS DOUBLE)     AS link_length_miles,
                estimation_method,
                CAST(pedal_cycles AS BIGINT)          AS pedal_cycles,
                CAST(two_wheeled_motor_vehicles AS BIGINT) AS two_wheeled_motor_vehicles,
                CAST(cars_and_taxis AS BIGINT)        AS cars_and_taxis,
                CAST(buses_and_coaches AS BIGINT)     AS buses_and_coaches,
                CAST("LGVs" AS BIGINT)                AS lgvs,
                CAST("all_HGVs" AS BIGINT)            AS all_hgvs,
                CAST(all_motor_vehicles AS BIGINT)    AS all_motor_vehicles
            FROM "{_AADF}"
            WHERE count_point_id IS NOT NULL AND year IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_AADF_DIR}-transform",
        deps=[_AADF_DIR],
        sql=f'''
            SELECT
                CAST(count_point_id AS BIGINT)        AS count_point_id,
                CAST(year AS INTEGER)                 AS year,
                direction_of_travel,
                CAST(region_id AS INTEGER)            AS region_id,
                region_name,
                region_ons_code,
                CAST(local_authority_id AS INTEGER)   AS local_authority_id,
                local_authority_name,
                local_authority_code,
                road_name,
                road_category,
                road_type,
                CAST(latitude AS DOUBLE)              AS latitude,
                CAST(longitude AS DOUBLE)             AS longitude,
                CAST(link_length_km AS DOUBLE)        AS link_length_km,
                estimation_method,
                CAST(pedal_cycles AS BIGINT)          AS pedal_cycles,
                CAST(two_wheeled_motor_vehicles AS BIGINT) AS two_wheeled_motor_vehicles,
                CAST(cars_and_taxis AS BIGINT)        AS cars_and_taxis,
                CAST(buses_and_coaches AS BIGINT)     AS buses_and_coaches,
                CAST("LGVs" AS BIGINT)                AS lgvs,
                CAST("all_HGVs" AS BIGINT)            AS all_hgvs,
                CAST(all_motor_vehicles AS BIGINT)    AS all_motor_vehicles
            FROM "{_AADF_DIR}"
            WHERE count_point_id IS NOT NULL AND year IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_RAW}-transform",
        deps=[_RAW],
        sql=f'''
            SELECT
                CAST(count_point_id AS BIGINT)        AS count_point_id,
                direction_of_travel,
                CAST(year AS INTEGER)                 AS year,
                CAST(count_date AS DATE)              AS count_date,
                CAST(hour AS INTEGER)                 AS hour,
                CAST(region_id AS INTEGER)            AS region_id,
                region_name,
                CAST(local_authority_id AS INTEGER)   AS local_authority_id,
                local_authority_name,
                road_name,
                road_category,
                road_type,
                CAST(pedal_cycles AS BIGINT)          AS pedal_cycles,
                CAST(two_wheeled_motor_vehicles AS BIGINT) AS two_wheeled_motor_vehicles,
                CAST(cars_and_taxis AS BIGINT)        AS cars_and_taxis,
                CAST(buses_and_coaches AS BIGINT)     AS buses_and_coaches,
                CAST("LGVs" AS BIGINT)                AS lgvs,
                CAST("all_HGVs" AS BIGINT)            AS all_hgvs,
                CAST(all_motor_vehicles AS BIGINT)    AS all_motor_vehicles
            FROM "{_RAW}"
            WHERE count_point_id IS NOT NULL AND count_date IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_LA}-transform",
        deps=[_LA],
        sql=f'''
            SELECT
                CAST(local_authority_id AS INTEGER)   AS local_authority_id,
                local_authority_name,
                local_authority_code,
                CAST(year AS INTEGER)                 AS year,
                CAST(link_length_km AS DOUBLE)        AS link_length_km,
                CAST(link_length_miles AS DOUBLE)     AS link_length_miles,
                CAST(cars_and_taxis AS DOUBLE)        AS cars_and_taxis,
                CAST(all_motor_vehicles AS DOUBLE)    AS all_motor_vehicles
            FROM "{_LA}"
            WHERE local_authority_id IS NOT NULL AND year IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_REGION_ROAD}-transform",
        deps=[_REGION_ROAD],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)                 AS year,
                CAST(region_id AS INTEGER)            AS region_id,
                region_name,
                region_ons_code,
                CAST(road_category_id AS INTEGER)     AS road_category_id,
                road_category_name,
                CAST(link_length_km AS DOUBLE)        AS link_length_km,
                CAST(link_length_miles AS DOUBLE)     AS link_length_miles,
                CAST(all_motor_vehicles AS DOUBLE)    AS all_motor_vehicles
            FROM "{_REGION_ROAD}"
            WHERE year IS NOT NULL AND region_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_REGION_VEH}-transform",
        deps=[_REGION_VEH],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)                 AS year,
                CAST(region_id AS INTEGER)            AS region_id,
                region_name,
                region_ons_code,
                CAST(link_length_km AS DOUBLE)        AS link_length_km,
                CAST(link_length_miles AS DOUBLE)     AS link_length_miles,
                CAST(pedal_cycles AS DOUBLE)          AS pedal_cycles,
                CAST(two_wheeled_motor_vehicles AS DOUBLE) AS two_wheeled_motor_vehicles,
                CAST(cars_and_taxis AS DOUBLE)        AS cars_and_taxis,
                CAST(buses_and_coaches AS DOUBLE)     AS buses_and_coaches,
                CAST("LGVs" AS DOUBLE)                AS lgvs,
                CAST("all_HGVs" AS DOUBLE)            AS all_hgvs,
                CAST(all_motor_vehicles AS DOUBLE)    AS all_motor_vehicles
            FROM "{_REGION_VEH}"
            WHERE year IS NOT NULL AND region_id IS NOT NULL
        ''',
    ),
]
