"""SteamDB most_played — weekly top-100 by peak CCU.

ISteamChartsService/GetMostPlayedGames. Stateless full re-pull of a one-shot
~100-row payload; current-state snapshot overwritten each run.
"""
from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import MOST_PLAYED_URL, _web_json

_MOST_PLAYED_SCHEMA = pa.schema([
    ("rank", pa.int32()),
    ("appid", pa.int64()),
    ("last_week_rank", pa.int32()),
    ("peak_in_game", pa.int64()),
    ("rollup_date", pa.timestamp("us", tz="UTC")),
])


def fetch_most_played(node_id: str) -> None:
    resp = _web_json(MOST_PLAYED_URL)["response"]
    rollup = datetime.fromtimestamp(int(resp.get("rollup_date") or 0), tz=timezone.utc)
    rows = [
        {
            "rank": int(r["rank"]),
            "appid": int(r["appid"]),
            "last_week_rank": int(r["last_week_rank"]) if r.get("last_week_rank") is not None else None,
            "peak_in_game": int(r.get("peak_in_game") or 0),
            "rollup_date": rollup,
        }
        for r in resp.get("ranks", [])
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_MOST_PLAYED_SCHEMA), node_id)
