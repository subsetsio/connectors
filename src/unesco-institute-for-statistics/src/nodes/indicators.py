"""UIS indicators catalog — one row per indicatorCode (reference subset)."""
import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import SLUG, fetch_indicators_list

_INDICATORS_SCHEMA = pa.schema([
    ("indicator_code", pa.string()),
    ("name", pa.string()),
    ("theme", pa.string()),
    ("last_data_update", pa.string()),
    ("last_data_update_description", pa.string()),
    ("total_record_count", pa.int64()),
    ("year_min", pa.int64()),
    ("year_max", pa.int64()),
    ("geo_unit_types", pa.string()),
])


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    inds = fetch_indicators_list()
    rows = []
    for i in inds:
        avail = i.get("dataAvailability") or {}
        timeline = avail.get("timeLine") or {}
        geo_types = (avail.get("geoUnits") or {}).get("types") or []
        rows.append({
            "indicator_code": i.get("indicatorCode"),
            "name": i.get("name"),
            "theme": i.get("theme"),
            "last_data_update": i.get("lastDataUpdate"),
            "last_data_update_description": i.get("lastDataUpdateDescription"),
            "total_record_count": avail.get("totalRecordCount"),
            "year_min": timeline.get("min"),
            "year_max": timeline.get("max"),
            "geo_unit_types": ",".join(geo_types) if geo_types else None,
        })
    table = pa.Table.from_pylist(rows, schema=_INDICATORS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-indicators", fn=fetch_indicators, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-indicators-transform",
        deps=[f"{SLUG}-indicators"],
        sql=f'''
            SELECT
                indicator_code,
                name,
                theme,
                last_data_update,
                last_data_update_description,
                CAST(total_record_count AS BIGINT) AS total_record_count,
                CAST(year_min AS INTEGER)          AS year_min,
                CAST(year_max AS INTEGER)          AS year_max,
                geo_unit_types
            FROM "{SLUG}-indicators"
            WHERE indicator_code IS NOT NULL
        ''',
    ),
]
