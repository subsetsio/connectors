"""United Nations — SDG series catalog (~713 release-tagged series).

Series/List is a single small JSON document; light array flattening
(series -> goal/target/indicator arrays) keeps the published table on a flat
NDJSON schema.
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import get_json, dedupe


def fetch_series(node_id: str) -> None:
    asset = node_id
    records = get_json("Series/List")
    if not isinstance(records, list) or not records:
        raise RuntimeError("Series/List returned no records")
    rows = []
    for r in records:
        goals = dedupe(r.get("goal"))
        targets = dedupe(r.get("target"))
        indicators = dedupe(r.get("indicator"))
        rows.append({
            "series_code": r.get("code"),
            "description": r.get("description"),
            "release": r.get("release"),
            "uri": r.get("uri"),
            "goals": ",".join(goals) if goals else None,
            "targets": ",".join(targets) if targets else None,
            "indicators": ",".join(indicators) if indicators else None,
        })
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="united-nations-series", fn=fetch_series, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="united-nations-series-transform",
        deps=["united-nations-series"],
        sql='''
            SELECT
                series_code,
                description,
                release,
                uri,
                goals,
                targets,
                indicators
            FROM "united-nations-series"
            WHERE series_code IS NOT NULL
        ''',
    ),
]
