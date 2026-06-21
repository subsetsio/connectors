"""GSoD Indicators — the GSoD indicator catalog.

code -> name/description/section, from /gsod-indices/api/labels. Reference
taxonomy for the GSoD Indices panel.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import GSOD_API, request


def fetch_gsod_indicators(node_id: str) -> None:
    asset = node_id
    resp = request(f"{GSOD_API}/labels")
    rows = resp.json()
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"GSoD /api/labels returned no rows: {str(rows)[:200]}")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="international-idea-gsod-indicators", fn=fetch_gsod_indicators, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="international-idea-gsod-indicators-transform",
        deps=["international-idea-gsod-indicators"],
        sql='''
            SELECT
                id                          AS indicator_code,
                name                        AS indicator_name,
                description,
                section                     AS parent_code,
                color,
                selectable,
                TRY_CAST("Weight" AS DOUBLE) AS weight
            FROM "international-idea-gsod-indicators"
            WHERE id IS NOT NULL
        ''',
    ),
]
