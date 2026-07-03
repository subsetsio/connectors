"""NHL API connector — NHL stats REST surface (api.nhle.com/stats/rest/en).

Catalog connector over the NHL stats REST API. Two kinds of entity:

* **reports** (50) — season-aggregated stat tables for skaters / goalies / teams.
  Each report has its own column list and is queried per season + game type:
  GET /{family}/{report}?limit=N&start=K&cayenneExp=seasonId=<id> and gameTypeId=<2|3>
  Broad (all-season) queries are server-capped at 10000 rows, so we fetch
  per-season and offset-paginate; one season+gameType is comfortably small.
  Regular season (gameTypeId=2) and playoffs (gameTypeId=3) are unioned, with
  gameTypeId injected onto each row so the transform can distinguish them.

* **reference** (3) — season / team / franchise catalogs (whole table in one
  request, no cayenneExp).

Fetch shape: stateless full re-pull (shape 1). The whole corpus is a few-tens-
of-thousands of rows per report across 108 immutable historical seasons plus
the live current season; re-pulling in full each run picks up the current
season's revisions for free. No incremental query filter is exposed.

Raw is NDJSON: the 50 reports each have a distinct column set (and columns drift
across eras), so a single shared fetch fn writes heterogeneous records rather
than 50 hand-declared parquet schemas.
"""

import urllib.parse


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://api.nhle.com/stats/rest/en"

# The authoritative coverage target — copied from
# data/sources/nhl/work/entity_union.json. One download spec per id.
from constants import ENTITY_IDS

# Whole-table reference catalogs: entity id -> REST resource path.
REFERENCE_PATHS = {
    "season": "season",
    "team": "team",
    "franchise": "franchise",
}

# Report endpoints whose REST path keeps the original camelCase config key —
# the lowercased entity-id form 500s, so these need an explicit mapping.
# (All other reports work with the plain "family/report" lowercase path.)
ENDPOINT_CASE = {
    "skater-scoringrates": "skater/scoringRates",
    "skater-penaltyshots": "skater/penaltyShots",
    "skater-puckpossessions": "skater/puckPossessions",
    "skater-goalsforagainst": "skater/goalsForAgainst",
    "goalie-startedvsrelieved": "goalie/startedVsRelieved",
    "goalie-savesbystrength": "goalie/savesByStrength",
    "goalie-penaltyshots": "goalie/penaltyShots",
    "team-savepercentage": "team/savePercentage",
}

# Regular season + playoffs. (Preseason gameTypeId=1 is excluded — sparse and
# not a meaningful statistical unit.)
GAME_TYPES = (2, 3)

# The API caps a positive `limit` at 100 rows/page, but `limit=-1` returns the
# entire result set in one request. A single season+gameType (or a reference
# catalog) is always well under the server's 10000-row hard cap, so `limit=-1`
# is one request per slice. PAGE is only the fallback page size if a `limit=-1`
# response ever comes back truncated.
PAGE = 100
MAX_OFFSET = 200_000  # safety ceiling — raises rather than looping forever


@transient_retry()
def _get_json(path: str, params: dict) -> dict:
    # cayenneExp must be sent pre-encoded (spaces around 'and'); build the query
    # string ourselves so httpx doesn't re-encode the expression inconsistently.
    qs = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    resp = get(f"{BASE}/{path}?{qs}", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _offset_pages(path: str, cayenne: str | None, total: int) -> list[dict]:
    """Fallback: walk the endpoint in 100-row pages until `total` is reached.
    Only used if a `limit=-1` response came back truncated (broad query past
    the server's 10000-row cap)."""
    rows: list[dict] = []
    start = 0
    while len(rows) < total:
        params = {"limit": PAGE, "start": start}
        if cayenne is not None:
            params["cayenneExp"] = cayenne
        batch = _get_json(path, params).get("data", []) or []
        if not batch:
            break
        rows.extend(batch)
        start += PAGE
        if start > MAX_OFFSET:
            raise RuntimeError(
                f"pagination runaway for {path} (cayenne={cayenne}) "
                f"past {MAX_OFFSET} rows"
            )
    return rows


def _paginate(path: str, cayenne: str | None) -> list[dict]:
    """Fetch a full stats report/catalog slice. `limit=-1` returns the whole
    result set in one request; fall back to offset paging only if that response
    is truncated."""
    params = {"limit": -1, "start": 0}
    if cayenne is not None:
        params["cayenneExp"] = cayenne
    payload = _get_json(path, params)
    data = payload.get("data", []) or []
    total = payload.get("total", 0) or 0
    if len(data) < total:
        data = _offset_pages(path, cayenne, total)
    return data


def _season_ids() -> list[int]:
    rows = _paginate("season", None)
    return [r["id"] for r in rows if r.get("id") is not None]


def _report_path(entity: str) -> str:
    if entity in ENDPOINT_CASE:
        return ENDPOINT_CASE[entity]
    family, report = entity.split("-", 1)
    return f"{family}/{report}"


def fetch_one(node_id: str) -> None:
    """Fetch one NHL stats entity. The runtime passes the spec id; it IS the
    asset name. Recover the entity by stripping the 'nhl-' prefix."""
    entity = node_id[len("nhl-"):]

    if entity in REFERENCE_PATHS:
        rows = _paginate(REFERENCE_PATHS[entity], None)
        save_raw_ndjson(rows, node_id)
        return

    # A season-aggregated stat report: union every season x game type.
    path = _report_path(entity)
    all_rows: list[dict] = []
    for season_id in _season_ids():
        for game_type in GAME_TYPES:
            cayenne = f"seasonId={season_id} and gameTypeId={game_type}"
            batch = _paginate(path, cayenne)
            for r in batch:
                # Stamp the game type — report rows carry seasonId but not the
                # game type that scoped the query.
                r["gameTypeId"] = game_type
            all_rows.extend(batch)
    save_raw_ndjson(all_rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"nhl-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Grain / observation-period per published table. The season-aggregated stat
# reports carry exactly one row per (playerId|teamId, seasonId, gameTypeId) —
# consistent row counts across reports confirm this. Bios reports aggregate a
# player across seasons (per gameType), so they have no seasonId. Reference
# catalogs are keyed on their surrogate `id`.
_REFERENCE_GRAIN = {
    "nhl-franchise": {"key": ("id",)},
    "nhl-team": {"key": ("id",)},
    "nhl-season": {"key": ("id",), "temporal": "endDate"},
}
_BIOS_IDS = {"nhl-goalie-bios", "nhl-skater-bios"}

GRAIN: dict[str, dict] = {}
for _s in DOWNLOAD_SPECS:
    if _s.id in _REFERENCE_GRAIN:
        GRAIN[_s.id] = _REFERENCE_GRAIN[_s.id]
    elif _s.id in _BIOS_IDS:
        GRAIN[_s.id] = {"key": ("playerId", "gameTypeId")}
    elif _s.id.startswith("nhl-team-"):
        GRAIN[_s.id] = {"key": ("seasonId", "teamId", "gameTypeId"), "temporal": "seasonId"}
    else:
        GRAIN[_s.id] = {"key": ("playerId", "seasonId", "gameTypeId"), "temporal": "seasonId"}

# Each report/catalog raw asset publishes one Delta table. The raw is already
# the clean tabular shape the source returns; the transform is a thin
# parse-and-publish pass (DuckDB types the NDJSON columns; a 0-row result fails
# the node, which is the correctness gate).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
        key=GRAIN.get(s.id, {}).get("key"),
        temporal=GRAIN.get(s.id, {}).get("temporal"),
    )
    for s in DOWNLOAD_SPECS
]
