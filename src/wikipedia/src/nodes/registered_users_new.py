"""Wikipedia AQS — monthly new registered users per project."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import BASE, START, collect_per_project, now_end, parse_nested, per_project_sql


def fetch_registered_users_new(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("new_registered_users", pa.int64()),
    ])

    def path_for(p):
        return f"{BASE}/registered-users/new/{p}/monthly/{START}/{end}"

    collect_per_project(node_id, path_for, parse_nested("new_registered_users"), schema)


DOWNLOAD_SPECS = [
    NodeSpec(id="wikipedia-registered-users-new", fn=fetch_registered_users_new, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wikipedia-registered-users-new-transform",
        deps=["wikipedia-registered-users-new"],
        sql=per_project_sql("wikipedia-registered-users-new", ["new_registered_users"]),
    ),
]
