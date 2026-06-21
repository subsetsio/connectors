"""Wikipedia AQS — monthly net bytes difference per project (aggregate)."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, START, collect_per_project, now_end, parse_nested, per_project_sql


def fetch_bytes_difference_net(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("net_bytes_diff", pa.int64()),
    ])

    def path_for(p):
        return (f"{BASE}/bytes-difference/net/aggregate/{p}/all-editor-types/"
                f"all-page-types/monthly/{START}/{end}")

    collect_per_project(node_id, path_for, parse_nested("net_bytes_diff"), schema)


DOWNLOAD_SPECS = [
    NodeSpec(id="wikipedia-bytes-difference-net", fn=fetch_bytes_difference_net, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wikipedia-bytes-difference-net-transform",
        deps=["wikipedia-bytes-difference-net"],
        sql=per_project_sql("wikipedia-bytes-difference-net", ["net_bytes_diff"]),
    ),
]
