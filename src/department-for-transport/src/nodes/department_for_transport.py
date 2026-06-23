"""Department for Transport (UK) — road-traffic statistics.

Chosen mechanism: roadtraffic_bulk_csv. Each subset is one stable object on the
public Google Cloud Storage bucket `dft-statistics` under the prefix
road-traffic/downloads/data-gov-uk/. Small aggregate datasets are plain CSV;
the large count-point datasets are a single CSV inside a ZIP. There is no
incremental query surface (no since/cursor) and the whole object is rewritten
in place on each annual release, so every node does a stateless full re-pull and
overwrites — revisions are picked up for free.

Raw is written as gzipped CSV (`<id>.csv.gz`), streamed straight from the source
(the ~1GB uncompressed raw_counts file never lands in memory). DuckDB reads the
CSV views directly in TRANSFORM_SPECS, where each subset is cast/renamed into its
published Delta table.
"""

import io
import shutil
import zipfile

from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_writer, transient_retry

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

_CHUNK = 8 * 1024 * 1024


@transient_retry()
def _fetch(url: str):
    # Read timeout is generous: raw_counts.zip is ~88MB over a single request.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the raw asset name
    filename = DATASETS[node_id]
    resp = _fetch(BASE + filename)

    if filename.endswith(".zip"):
        zf = zipfile.ZipFile(io.BytesIO(resp.content))
        member = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
        with zf.open(member) as src, raw_writer(
            asset, "csv.gz", mode="wb", compression="gzip"
        ) as dst:
            shutil.copyfileobj(src, dst, length=_CHUNK)
    else:
        with raw_writer(asset, "csv.gz", mode="wb", compression="gzip") as dst:
            dst.write(resp.content)


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
