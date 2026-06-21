"""Wikipedia AQS — monthly absolute bytes difference per project (aggregate)."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, START, collect_per_project, now_end, parse_nested, per_project_sql


def fetch_bytes_difference_absolute(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("abs_bytes_diff", pa.int64()),
    ])

    def path_for(p):
        return (f"{BASE}/bytes-difference/absolute/aggregate/{p}/all-editor-types/"
                f"all-page-types/monthly/{START}/{end}")

    collect_per_project(node_id, path_for, parse_nested("abs_bytes_diff"), schema)


DOWNLOAD_SPECS = [
    NodeSpec(id="wikipedia-bytes-difference-absolute", fn=fetch_bytes_difference_absolute, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wikipedia-bytes-difference-absolute-transform",
        deps=["wikipedia-bytes-difference-absolute"],
        sql=per_project_sql("wikipedia-bytes-difference-absolute", ["abs_bytes_diff"]),
    ),
]
