"""Data.gov organizations — publishing-org taxonomy (reference, ~132 rows).

Distinct fetch shape from the package corpus: organization_list?all_fields
paged by offset (caps at 25 per page). Single ndjson batch.
"""

from subsets_utils import NodeSpec, save_raw_ndjson
from utils import _action

ORG_PAGE = 25             # organization_list?all_fields caps at 25 per offset


def fetch_organizations(node_id: str) -> None:
    asset = node_id
    rows: list[dict] = []
    offset = 0
    while True:
        page = _action("organization_list", all_fields="true", limit=ORG_PAGE, offset=offset)
        if not page:
            break
        for o in page:
            rows.append({
                "id": o.get("id"),
                "name": o.get("name"),
                "title": o.get("title"),
                "display_name": o.get("display_name"),
                "description": o.get("description"),
                "package_count": o.get("package_count"),
                "organization_type": o.get("organization_type"),
                "type": o.get("type"),
                "state": o.get("state"),
                "created": o.get("created"),
                "num_followers": o.get("num_followers"),
                "is_organization": o.get("is_organization"),
                "approval_status": o.get("approval_status"),
            })
        offset += len(page)
        if len(page) < ORG_PAGE:
            break
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="data-gov-organizations", fn=fetch_organizations, kind="download"),
]
