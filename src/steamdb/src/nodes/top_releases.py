"""SteamDB top_releases — top new releases per month.

ISteamChartsService/GetTopReleasesPages. Stateless full re-pull; current-state
snapshot overwritten each run.
"""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import TOP_RELEASES_URL, _web_json

_TOP_RELEASES_SCHEMA = pa.schema([
    ("month_name", pa.string()),
    ("start_of_month", pa.int64()),  # epoch seconds; transform -> timestamp
    ("rank", pa.int32()),
    ("appid", pa.int64()),
])


def fetch_top_releases(node_id: str) -> None:
    resp = _web_json(TOP_RELEASES_URL)["response"]
    rows = []
    for p in resp.get("pages", []):
        som = int(p.get("start_of_month") or 0)
        name = p.get("name") or ""
        for i, it in enumerate(p.get("item_ids", []), start=1):
            rows.append({
                "month_name": name,
                "start_of_month": som,
                "rank": i,
                "appid": int(it["appid"]),
            })
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_TOP_RELEASES_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="steamdb-top-releases", fn=fetch_top_releases, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="steamdb-top-releases-transform",
        deps=["steamdb-top-releases"],
        sql='''
            SELECT
                month_name,
                to_timestamp(start_of_month) AS start_of_month,
                CAST(rank AS INTEGER)        AS rank,
                CAST(appid AS BIGINT)        AS appid
            FROM "steamdb-top-releases"
            WHERE appid IS NOT NULL
            ORDER BY start_of_month DESC, rank
        ''',
    ),
]
