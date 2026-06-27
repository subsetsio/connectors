"""NHL public stats API connector (api.nhle.com/stats/rest/en).

Catalog connector: one download node per (entity-family, report) statistical
table plus a few reference dimension tables. The fetch surface is the
`stats_rest` mechanism chosen by research.

Fetch strategy — stateless full re-pull every run:
  * Report tables (/{entity}/{report}) require a mandatory cayenneExp filter
    selecting seasonId + gameTypeId (omitting it returns HTTP 500). The server
    masks results: a positive `limit` is capped at 100 rows/page and `limit=-1`
    is capped at 10000 rows while reporting total=10000 (verified). Neither
    paginates the full history safely. So we page PER SEASON: one limit=-1
    request per (season, gameType), each comfortably under the 10000 cap
    (largest observed season ~1000 rows). gameTypeId is NOT echoed in rows, so
    we inject it. Season list is discovered from /season, never hardcoded.
  * Reference tables (/season, /team, /franchise) take no filter and return
    their full small table in one request.

Raw is written as NDJSON: 50 report schemas differ from each other and null
patterns drift across seasons within a report, so the no-schema NDJSON path is
the safe choice (the SQL transform re-types on read).
"""

import pyarrow as pa  # noqa: F401  (kept for parity; not required for ndjson)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_IDS, ENTITY_FETCH

BASE = "https://api.nhle.com/stats/rest/en"

# Safety ceiling: per (season, gameType) a report should be far under the
# server's 10000-row response cap. Hitting it means the cap silently truncated
# a single season — raise rather than publish a partial table.
SEASON_ROW_CEILING = 10000


@transient_retry()  # 6 attempts, exponential backoff over 429/5xx/transient net
def _get_json(path: str, **params):
    resp = get(f"{BASE}{path}", params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _season_ids() -> list[int]:
    return [s["id"] for s in _get_json("/season")["data"]]


def _fetch_report(path: str) -> list[dict]:
    """Full league history for one report: per-season, per-gameType, with the
    gameTypeId injected onto every row (the API does not echo it)."""
    rows: list[dict] = []
    for season_id in _season_ids():
        for game_type_id in (2, 3):  # 2=regular season, 3=playoffs
            data = _get_json(
                path,
                limit=-1,
                cayenneExp=f"seasonId={season_id} and gameTypeId={game_type_id}",
            )["data"]
            if len(data) >= SEASON_ROW_CEILING:
                raise RuntimeError(
                    f"{path} season={season_id} gameType={game_type_id} returned "
                    f"{len(data)} rows (>= {SEASON_ROW_CEILING} cap) — response "
                    "likely truncated; per-season paging assumption broken."
                )
            for row in data:
                row["gameTypeId"] = game_type_id
            rows.extend(data)
    return rows


def _fetch_reference(path: str) -> list[dict]:
    return _get_json(path)["data"]


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime hands us the spec id; it IS the asset name
    entity_id = node_id[len("nhl-api-"):]
    kind, path = ENTITY_FETCH[entity_id]
    if kind == "report":
        rows = _fetch_report(path)
    else:
        rows = _fetch_reference(path)
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"nhl-api-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per download. Each report/reference already arrives
# as clean tabular rows; the transform is a thin typed pass-through (DuckDB
# infers types off the NDJSON, the 0-row gate guards correctness). gameTypeId
# and seasonId travel as columns on every report table.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
