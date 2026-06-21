"""Wikipedia AQS — monthly edits per project (aggregate)."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, START, collect_per_project, now_end, parse_nested, per_project_sql


def fetch_edits(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("edits", pa.int64()),
    ])

    def path_for(p):
        return (f"{BASE}/edits/aggregate/{p}/all-editor-types/all-page-types/"
                f"monthly/{START}/{end}")

    collect_per_project(node_id, path_for, parse_nested("edits"), schema)


DOWNLOAD_SPECS = [
    NodeSpec(id="wikipedia-edits", fn=fetch_edits, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wikipedia-edits-transform",
        deps=["wikipedia-edits"],
        sql=per_project_sql("wikipedia-edits", ["edits"]),
    ),
]
