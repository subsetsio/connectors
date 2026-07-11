"""Realtime Inequality (Blanchet, Saez & Zucman) — US distributional national accounts.

All website data is served as a handful of static JSON files from a public
Cloudflare R2 bucket. Each file is small (a few hundred KB to ~12 MB) and
returns its full content in one GET, so the correct shape is a stateless full
re-pull every run — no watermark, no incremental query (the source exposes
none). Raw is written as NDJSON to preserve the source's nulls (many income
concepts are null for demographic breakdowns that don't compute them) and to
tolerate the occasional int/float drift in numeric columns; the SQL transforms
re-type on read.
"""


from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

_BUCKET = "https://pub-718b8afebf4a450498e2111e3bbf4901.r2.dev"

# spec-id (minus the slug prefix) -> source path under the bucket.
_PATHS = {
    "online-database": "temp_data/online-database.json",
    "online-database-labor": "temp_data/online-database-labor.json",
    "online-database-demographics": "temp_data/online-database-demographics.json",
    "online-database-popul-deflator": "temp_data/online-database-popul-deflator.json",
    "wealth-projection": "projection/wealth_update.json",
}


def _fetch_json(url: str):
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("realtime-inequality-"):]
    payload = _fetch_json(f"{_BUCKET}/{_PATHS[entity]}")
    rows = payload["data"] if isinstance(payload, dict) else payload
    if not rows:
        raise AssertionError(f"{asset}: source returned no rows")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"realtime-inequality-{entity}", fn=fetch_one, kind="download")
    for entity in _PATHS
]
