"""UIS geographic units — countries + regional aggregates (taxonomy subset)."""
import pyarrow as pa
from subsets_utils import save_raw_parquet
from utils import get_json

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

