"""UIS geographic units — countries + regional aggregates (taxonomy subset)."""
import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import SLUG, get_json

_GEOUNITS_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("name", pa.string()),
    ("type", pa.string()),
    ("region_group", pa.string()),
])


def fetch_geounits(node_id: str) -> None:
    asset = node_id
    data = get_json("definitions/geounits")
    if not isinstance(data, list) or not data:
        raise AssertionError(f"geounits endpoint returned {type(data).__name__} (empty?)")
    rows = [{
        "id": g.get("id"),
        "name": g.get("name"),
        "type": g.get("type"),
        "region_group": g.get("regionGroup"),
    } for g in data]
    table = pa.Table.from_pylist(rows, schema=_GEOUNITS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-geounits", fn=fetch_geounits, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-geounits-transform",
        deps=[f"{SLUG}-geounits"],
        sql=f'''
            SELECT
                id,
                name,
                type,
                region_group
            FROM "{SLUG}-geounits"
            WHERE id IS NOT NULL
        ''',
    ),
]
