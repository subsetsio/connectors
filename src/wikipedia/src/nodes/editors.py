"""Wikipedia AQS — monthly active editors per project (aggregate)."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, START, collect_per_project, now_end, parse_nested, per_project_sql


def fetch_editors(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("editors", pa.int64()),
    ])

    def path_for(p):
        return (f"{BASE}/editors/aggregate/{p}/all-editor-types/all-page-types/"
                f"all-activity-levels/monthly/{START}/{end}")

    collect_per_project(node_id, path_for, parse_nested("editors"), schema)


DOWNLOAD_SPECS = [
    NodeSpec(id="wikipedia-editors", fn=fetch_editors, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wikipedia-editors-transform",
        deps=["wikipedia-editors"],
        sql=per_project_sql("wikipedia-editors", ["editors"]),
    ),
]
