"""Sveriges Riksbank — SWEA series groups.

`groups` — reference metadata for every group used by the SWEA series catalog.
"""

import json

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import BASE, fetch_series_catalog, get_json

GROUPS_SCHEMA = pa.schema([
    ("group_id", pa.int64()),
    ("name", pa.string()),
    ("description", pa.string()),
    ("child_group_ids", pa.string()),
])


def fetch_groups(node_id: str) -> None:
    series = fetch_series_catalog()
    group_ids = sorted({s.get("groupId") for s in series if s.get("groupId") is not None})
    rows = []

    for group_id in group_ids:
        group = get_json(f"{BASE}/Groups/{group_id}")
        children = group.get("childGroups") or []
        child_ids = [
            child.get("groupId")
            for child in children
            if isinstance(child, dict) and child.get("groupId") is not None
        ]
        rows.append(
            {
                "group_id": group.get("groupId"),
                "name": group.get("name"),
                "description": group.get("description"),
                "child_group_ids": json.dumps(child_ids, separators=(",", ":")),
            }
        )

    if not rows:
        raise AssertionError("fetched 0 groups from SWEA group endpoints")

    table = pa.Table.from_pylist(rows, schema=GROUPS_SCHEMA)
    save_raw_parquet(table, node_id)
