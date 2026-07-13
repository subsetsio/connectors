"""SteamDB app_reviews — per-app aggregate review summary.

store appreviews over the union of appids across the three charts. Throttled
store host (~16/min per process). Current-state snapshot overwritten each run.
"""
import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import STORE_API, _chart_appids, _store_json_limited

_APP_REVIEWS_SCHEMA = pa.schema([
    ("appid", pa.int64()),
    ("review_score", pa.int32()),
    ("review_score_desc", pa.string()),
    ("total_positive", pa.int64()),
    ("total_negative", pa.int64()),
    ("total_reviews", pa.int64()),
])


def fetch_app_reviews(node_id: str) -> None:
    rows = []
    for appid in _chart_appids():
        body = _store_json_limited(
            f"{STORE_API}/appreviews/{appid}?json=1&num_per_page=0&language=all&purchase_type=all"
        )
        if not body.get("success"):
            continue
        qs = body.get("query_summary") or {}
        if not qs or qs.get("total_reviews") is None:
            continue
        rows.append({
            "appid": int(appid),
            "review_score": int(qs["review_score"]) if qs.get("review_score") is not None else None,
            "review_score_desc": qs.get("review_score_desc"),
            "total_positive": int(qs.get("total_positive") or 0),
            "total_negative": int(qs.get("total_negative") or 0),
            "total_reviews": int(qs.get("total_reviews") or 0),
        })
    if not rows:
        raise AssertionError("app_reviews produced 0 rows; store appreviews likely throttled/blocked")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_APP_REVIEWS_SCHEMA), node_id)

