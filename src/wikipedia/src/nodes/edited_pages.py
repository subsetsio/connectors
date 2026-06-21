"""Wikipedia AQS — monthly edited pages per project (aggregate)."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, START, collect_per_project, now_end, parse_nested, per_project_sql


def fetch_edited_pages(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("edited_pages", pa.int64()),
    ])

    def path_for(p):
        return (f"{BASE}/edited-pages/aggregate/{p}/all-editor-types/all-page-types/"
                f"all-activity-levels/monthly/{START}/{end}")

    collect_per_project(node_id, path_for, parse_nested("edited_pages"), schema)


DOWNLOAD_SPECS = [
    NodeSpec(id="wikipedia-edited-pages", fn=fetch_edited_pages, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wikipedia-edited-pages-transform",
        deps=["wikipedia-edited-pages"],
        sql=per_project_sql("wikipedia-edited-pages", ["edited_pages"]),
    ),
]
