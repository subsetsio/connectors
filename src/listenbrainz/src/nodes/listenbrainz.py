"""ListenBrainz connector — sitewide listening statistics.

Mechanism: rest_stats (https://api.listenbrainz.org, no auth needed for read).
Each publishable subset is one sitewide statistics endpoint. For every endpoint
we pull a fixed set of aggregation windows (the `range` parameter) and stack the
rows, tagging each with its `range` — so `range` becomes a column rather than a
basis for fanning out into separate datasets.

Shape: stateless full re-pull. The whole corpus per endpoint is a handful of
small precomputed aggregates (tens to ~1000 rows per range), trivially re-fetched
each run; there is no incremental delta to track (the `range` parameter selects a
precomputed window, not a since-cursor). The entity-top endpoints expose
hundreds-of-thousands of entities; we deliberately publish the top-N charts
(TOP_N per range, the API's single-page max), not the full long tail.

Raw is written as NDJSON because several endpoints carry nested/list fields
(artist_mbids lists, albums/artists sub-arrays) and field presence varies across
endpoints; the SQL transform flattens and types each subset.
"""

from datetime import datetime, timezone

import pyarrow as pa  # noqa: F401  (kept for parity; not required)
from subsets_utils import NodeSpec, get, save_raw_ndjson, transient_retry

BASE = "https://api.listenbrainz.org"

# Aggregation windows to pull per endpoint. Each becomes a value of the `range`
# column. These are the well-defined rolling windows; the calendar-to-date
# variants (this_week/this_month/this_year) are intentionally omitted as
# redundant with week/month/year.
RANGES = ["week", "month", "quarter", "half_yearly", "year", "all_time"]

# Top-N to request for the entity-top endpoints. 1000 is the API's single-page
# max (all_time recordings is hard-capped at 1000 server-side). We publish the
# top charts, not the full multi-hundred-thousand-entity tail.
TOP_N = 1000

# How to fetch each entity: endpoint path, the payload array key, and whether the
# endpoint accepts the `count` paging parameter (entity-top endpoints do).
ENDPOINTS = {
    "sitewide-artists": {"path": "/1/stats/sitewide/artists", "array_key": "artists", "has_count": True},
    "sitewide-releases": {"path": "/1/stats/sitewide/releases", "array_key": "releases", "has_count": True},
    "sitewide-release-groups": {"path": "/1/stats/sitewide/release-groups", "array_key": "release_groups", "has_count": True},
    "sitewide-recordings": {"path": "/1/stats/sitewide/recordings", "array_key": "recordings", "has_count": True},
    "sitewide-listening-activity": {"path": "/1/stats/sitewide/listening-activity", "array_key": "listening_activity", "has_count": False},
    "sitewide-artist-activity": {"path": "/1/stats/sitewide/artist-activity", "array_key": "artist_activity", "has_count": False},
    "sitewide-era-activity": {"path": "/1/stats/sitewide/era-activity", "array_key": "era_activity", "has_count": False},
    "sitewide-artist-map": {"path": "/1/stats/sitewide/artist-map", "array_key": "artist_map", "has_count": False},
}


@transient_retry()
def _fetch_payload(path: str, rng: str, has_count: bool):
    """Fetch one endpoint+range. Returns the `payload` dict, or None on HTTP 204
    (stat not yet computed for this window — treated as empty, not an error)."""
    params = {"range": rng}
    if has_count:
        params["count"] = TOP_N
    resp = get(f"{BASE}{path}", params=params, timeout=(10.0, 120.0))
    if resp.status_code == 204:
        return None
    resp.raise_for_status()
    return resp.json()["payload"]


def _epoch_date(value):
    if value is None:
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc).date().isoformat()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("listenbrainz-"):]
    cfg = ENDPOINTS[entity]

    rows = []
    for rng in RANGES:
        payload = _fetch_payload(cfg["path"], rng, cfg["has_count"])
        if payload is None:
            continue  # 204: window not computed yet
        items = payload.get(cfg["array_key"]) or []
        window = {
            "range": rng,
            "window_from_ts": payload.get("from_ts"),
            "window_to_ts": payload.get("to_ts"),
            "last_updated": payload.get("last_updated"),
            "last_updated_date": _epoch_date(payload.get("last_updated")),
        }
        for it in items:
            rows.append({**it, **window})

    if not rows:
        raise RuntimeError(f"{asset}: no rows across any of ranges {RANGES}")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="listenbrainz-sitewide-artists", fn=fetch_one, kind="download"),
    NodeSpec(id="listenbrainz-sitewide-releases", fn=fetch_one, kind="download"),
    NodeSpec(id="listenbrainz-sitewide-release-groups", fn=fetch_one, kind="download"),
    NodeSpec(id="listenbrainz-sitewide-recordings", fn=fetch_one, kind="download"),
    NodeSpec(id="listenbrainz-sitewide-listening-activity", fn=fetch_one, kind="download"),
    NodeSpec(id="listenbrainz-sitewide-artist-activity", fn=fetch_one, kind="download"),
    NodeSpec(id="listenbrainz-sitewide-era-activity", fn=fetch_one, kind="download"),
    NodeSpec(id="listenbrainz-sitewide-artist-map", fn=fetch_one, kind="download"),
]
