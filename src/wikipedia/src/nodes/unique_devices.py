"""Wikipedia AQS — monthly unique devices per project (all-sites)."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, START, collect_per_project, now_end, per_project_sql, to_date


def fetch_unique_devices(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("devices", pa.int64()),
        ("offset", pa.int64()),
        ("underestimate", pa.int64()),
    ])

    def path_for(p):
        return f"{BASE}/unique-devices/{p}/all-sites/monthly/{START}/{end}"

    def parse_into(data, rows):
        for it in data.get("items", []):
            rows.append({
                "project": it["project"],
                "date": to_date(it["timestamp"]),
                "devices": it.get("devices"),
                "offset": it.get("offset"),
                "underestimate": it.get("underestimate"),
            })

    collect_per_project(node_id, path_for, parse_into, schema)


DOWNLOAD_SPECS = [
    NodeSpec(id="wikipedia-unique-devices", fn=fetch_unique_devices, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wikipedia-unique-devices-transform",
        deps=["wikipedia-unique-devices"],
        sql=per_project_sql("wikipedia-unique-devices", ["devices", "offset", "underestimate"]),
    ),
]
