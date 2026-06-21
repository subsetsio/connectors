"""United Nations — SDG indicator framework (~251 indicators).

Indicator/List is a single small JSON document; light array flattening
(indicator -> series codes) keeps the published table on a flat NDJSON schema.
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import get_json, dedupe


def fetch_indicators(node_id: str) -> None:
    asset = node_id
    records = get_json("Indicator/List")
    if not isinstance(records, list) or not records:
        raise RuntimeError(f"Indicator/List returned no records (type={type(records).__name__})")
    rows = []
    for r in records:
        series = r.get("series") or []
        codes = dedupe([s.get("code") for s in series if s.get("code")])
        rows.append({
            "indicator_code": r.get("code"),
            "goal_code": r.get("goal"),
            "target_code": r.get("target"),
            "description": r.get("description"),
            "tier": r.get("tier"),
            "uri": r.get("uri"),
            "series_count": len(codes),
            "series_codes": ",".join(codes) if codes else None,
        })
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="united-nations-indicators", fn=fetch_indicators, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="united-nations-indicators-transform",
        deps=["united-nations-indicators"],
        sql='''
            SELECT
                indicator_code,
                goal_code,
                target_code,
                description,
                tier,
                uri,
                CAST(series_count AS INTEGER) AS series_count,
                series_codes
            FROM "united-nations-indicators"
            WHERE indicator_code IS NOT NULL
        ''',
    ),
]
