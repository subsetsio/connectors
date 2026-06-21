"""Shared HTTP + discovery helpers for the UNESCO UIS connector.

The public UIS Data API (https://api.uis.unesco.org/api/public/) is JSON, no
auth. `get_json` is the single retrying request helper; `fetch_indicators_list`
is the indicator-catalog discovery call shared by both the `indicators` and
`values` subsets (values fetches one request per indicator code).
"""
from subsets_utils import get, transient_retry

BASE = "https://api.uis.unesco.org/api/public"
SLUG = "unesco-institute-for-statistics"


@transient_retry()
def get_json(path: str, params: dict | None = None):
    resp = get(f"{BASE}/{path}", params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def fetch_indicators_list() -> list[dict]:
    data = get_json("definitions/indicators")
    if not isinstance(data, list) or not data:
        raise AssertionError(f"indicators endpoint returned {type(data).__name__} (empty?)")
    return data
