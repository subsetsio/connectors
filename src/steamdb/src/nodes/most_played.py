"""SteamDB most_played — weekly top-100 by peak CCU.

ISteamChartsService/GetMostPlayedGames. Stateless full re-pull of a one-shot
~100-row payload; current-state snapshot overwritten each run.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import MOST_PLAYED_URL, _web_json

_MOST_PLAYED_SCHEMA = pa.schema([
    ("rank", pa.int32()),
    ("appid", pa.int64()),
    ("last_week_rank", pa.int32()),
    ("peak_in_game", pa.int64()),
    ("rollup_date", pa.int64()),  # epoch seconds; transform -> timestamp
])


def fetch_most_played(node_id: str) -> None:
    resp = _web_json(MOST_PLAYED_URL)["response"]
    rollup = int(resp.get("rollup_date") or 0)
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


DOWNLOAD_SPECS = [
    NodeSpec(id="steamdb-most-played", fn=fetch_most_played, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="steamdb-most-played-transform",
        deps=["steamdb-most-played"],
        sql='''
            SELECT
                CAST(rank AS INTEGER)            AS rank,
                CAST(appid AS BIGINT)            AS appid,
                CAST(last_week_rank AS INTEGER)  AS last_week_rank,
                CAST(peak_in_game AS BIGINT)     AS peak_in_game,
                to_timestamp(rollup_date)        AS rollup_date
            FROM "steamdb-most-played"
            WHERE appid IS NOT NULL
            ORDER BY rank
        ''',
    ),
]
