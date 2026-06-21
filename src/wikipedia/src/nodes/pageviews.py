"""Wikipedia AQS — monthly pageviews per project (aggregate, all-access)."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, START, collect_per_project, now_end, per_project_sql, to_date


def fetch_pageviews(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("views", pa.int64()),
    ])

    def path_for(p):
        return f"{BASE}/pageviews/aggregate/{p}/all-access/all-agents/monthly/{START}/{end}"

    def parse_into(data, rows):
        for it in data.get("items", []):
            rows.append({
                "project": it["project"],
                "date": to_date(it["timestamp"]),
                "views": it.get("views"),
            })

    collect_per_project(node_id, path_for, parse_into, schema)


DOWNLOAD_SPECS = [
    NodeSpec(id="wikipedia-pageviews", fn=fetch_pageviews, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wikipedia-pageviews-transform",
        deps=["wikipedia-pageviews"],
        sql=per_project_sql("wikipedia-pageviews", ["views"]),
    ),
]
