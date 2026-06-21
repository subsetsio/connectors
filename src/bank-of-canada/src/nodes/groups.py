"""Bank of Canada — groups subset.

Reference catalog of ~2,400 named series groups (/lists/groups/json), one row
per group. Stateless full re-pull.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import BASE, _fetch_json

GROUPS_SCHEMA = pa.schema([
    ("group_id", pa.string()),
    ("label", pa.string()),
    ("description", pa.string()),
])


def fetch_groups(node_id: str) -> None:
    asset = node_id
    payload = _fetch_json(f"{BASE}/lists/groups/json")
    groups = payload["groups"]
    rows = [
        {
            "group_id": gid,
            "label": (meta.get("label") or "").strip() or None,
            "description": (meta.get("description") or "").strip() or None,
        }
        for gid, meta in groups.items()
    ]
    assert rows, "groups list returned no entries"
    table = pa.Table.from_pylist(rows, schema=GROUPS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="bank-of-canada-groups", fn=fetch_groups, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="bank-of-canada-groups-transform",
        deps=["bank-of-canada-groups"],
        sql='''
            SELECT
                group_id,
                label,
                description
            FROM "bank-of-canada-groups"
            WHERE group_id IS NOT NULL
        ''',
    ),
]
