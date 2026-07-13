"""SteamDB top_releases — top new releases per month.

ISteamChartsService/GetTopReleasesPages. Stateless full re-pull; current-state
snapshot overwritten each run.
"""
from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import TOP_RELEASES_URL, _web_json

_TOP_RELEASES_SCHEMA = pa.schema([
    ("month_name", pa.string()),
    ("start_of_month", pa.timestamp("us", tz="UTC")),
    ("rank", pa.int32()),
    ("appid", pa.int64()),
])


def fetch_top_releases(node_id: str) -> None:
    resp = _web_json(TOP_RELEASES_URL)["response"]
    rows = []
    for p in resp.get("pages", []):
        som = datetime.fromtimestamp(int(p.get("start_of_month") or 0), tz=timezone.utc)
        name = p.get("name") or ""
        for i, it in enumerate(p.get("item_ids", []), start=1):
            rows.append({
                "month_name": name,
                "start_of_month": som,
                "rank": i,
                "appid": int(it["appid"]),
            })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_TOP_RELEASES_SCHEMA), node_id)
