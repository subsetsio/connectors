"""SteamDB concurrent_players — live top-100 by current CCU.

ISteamChartsService/GetGamesByConcurrentPlayers. Stateless full re-pull of a
one-shot ~100-row payload; current-state snapshot overwritten each run.
"""
import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import CONCURRENT_URL, _web_json

_CONCURRENT_SCHEMA = pa.schema([
    ("rank", pa.int32()),
    ("appid", pa.int64()),
    ("concurrent_in_game", pa.int64()),
    ("peak_in_game", pa.int64()),
    ("last_update", pa.int64()),  # epoch seconds; transform -> timestamp
])


def fetch_concurrent_players(node_id: str) -> None:
    resp = _web_json(CONCURRENT_URL)["response"]
    ts = int(resp.get("last_update") or 0)
    rows = [
        {
            "rank": int(r["rank"]),
            "appid": int(r["appid"]),
            "concurrent_in_game": int(r["concurrent_in_game"]),
            "peak_in_game": int(r.get("peak_in_game") or 0),
            "last_update": ts,
        }
        for r in resp.get("ranks", [])
    ]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_CONCURRENT_SCHEMA), node_id)

