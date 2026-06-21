"""L2Beat projects — reference catalog, one row per tracked scaling project."""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import SUMMARY_URL, _get_json

_PROJECTS_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("name", pa.string()),
    ("slug", pa.string()),
    ("type", pa.string()),
    ("host_chain", pa.string()),
    ("category", pa.string()),
    ("stage", pa.string()),
    ("is_archived", pa.bool_()),
    ("is_under_review", pa.bool_()),
    ("providers", pa.string()),
    ("purposes", pa.string()),
    ("current_tvs_usd", pa.float64()),
])


def _coerce_tvs(value) -> float | None:
    """The summary `tvs` field is {"breakdown": {"total": <usd>, ...}, ...}."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        bd = value.get("breakdown")
        if isinstance(bd, dict):
            t = bd.get("total")
            if isinstance(t, (int, float)) and not isinstance(t, bool):
                return float(t)
        for k in ("total", "tvs", "usdValue", "value"):
            v = value.get(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return float(v)
    return None


def _join_list(value) -> str | None:
    if isinstance(value, list) and value:
        parts = [str(x) for x in value if x is not None]
        return ", ".join(parts) if parts else None
    return None


def fetch_projects(node_id: str) -> None:
    asset = node_id
    summary = _get_json(SUMMARY_URL)
    projects = summary["projects"]
    rows = []
    for slug, p in projects.items():
        rows.append({
            "id": str(p.get("id") or slug),
            "name": str(p.get("name") or slug),
            "slug": str(p.get("slug") or slug),
            "type": p.get("type"),
            "host_chain": p.get("hostChain"),
            "category": p.get("category"),
            "stage": None if p.get("stage") is None else str(p.get("stage")),
            "is_archived": bool(p.get("isArchived", False)),
            "is_under_review": bool(p.get("isUnderReview", False)),
            "providers": _join_list(p.get("providers")),
            "purposes": _join_list(p.get("purposes")),
            "current_tvs_usd": _coerce_tvs(p.get("tvs")),
        })
    table = pa.Table.from_pylist(rows, schema=_PROJECTS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="l2beat-projects", fn=fetch_projects, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="l2beat-projects-transform",
        deps=["l2beat-projects"],
        sql='''
            SELECT
                id,
                name,
                slug,
                type,
                host_chain,
                category,
                stage,
                is_archived,
                is_under_review,
                providers,
                purposes,
                current_tvs_usd
            FROM "l2beat-projects"
        ''',
    ),
]
