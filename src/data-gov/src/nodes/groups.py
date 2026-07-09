"""Data.gov groups - small topical taxonomy."""

from subsets_utils import save_raw_ndjson
from utils import _action


def fetch_groups(node_id: str) -> None:
    rows: list[dict] = []
    for g in _action("group_list", all_fields="true"):
        rows.append({
            "id": g.get("id"),
            "name": g.get("name"),
            "title": g.get("title"),
            "display_name": g.get("display_name"),
            "description": g.get("description"),
            "package_count": g.get("package_count"),
            "type": g.get("type"),
            "state": g.get("state"),
            "created": g.get("created"),
            "num_followers": g.get("num_followers"),
            "is_organization": g.get("is_organization"),
            "approval_status": g.get("approval_status"),
        })
    save_raw_ndjson(rows, node_id)
