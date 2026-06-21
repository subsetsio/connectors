"""MLB Stats API connector — season-aggregate statistics + standings.

Single public REST API at https://statsapi.mlb.com/api/v1/ (no auth). Strategy
is a stateless full re-pull: every refresh iterates the complete season set
(discovered from /seasons/all?sportId=1, currently 1876..present) and pulls the
full result for each season, concatenating into one raw asset per subset.
Season is a column, not a separate asset. There is no incremental filter and no
bulk export, so the whole corpus is re-fetched each run; it is a few thousand
rows per season-group and completes in minutes.

Seven subsets, each its own column schema:
  - standings                     team-season win/loss/run records
  - team-{hitting,pitching,fielding}   team-season aggregate stat lines
  - player-{hitting,pitching,fielding} player-season stat lines (playerPool=all)

Raw is saved as NDJSON (nested/heterogeneous source records, many optional stat
fields). Identity columns (season + ids) are stored as real ints for stable
typing; all other stat values are stored as strings and TRY_CAST in the SQL
transform, which is the correctness gate (bad shape fails loudly, 0 rows fails
the node).
"""

import pyarrow as pa  # noqa: F401  (kept for parity; ndjson path used)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)

BASE = "https://statsapi.mlb.com/api/v1"
HEADERS = {"Accept": "application/json"}  # some proxies 406 without this
PAGE_LIMIT = 5000
MAX_OFFSET = 500_000  # safety ceiling; a real season is < 3000 splits


@transient_retry()  # 6 attempts, exp backoff on 429/5xx/transient network
def _get_json(path: str, params: dict) -> dict:
    resp = get(f"{BASE}/{path}", params=params, headers=HEADERS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _all_seasons() -> list:
    """Every season id for MLB (sportId=1), ascending. Discovered, not hardcoded."""
    data = _get_json("seasons/all", {"sportId": 1})
    years = sorted(int(s["seasonId"]) for s in data.get("seasons", []))
    if len(years) < 50:
        raise RuntimeError(f"seasons/all returned only {len(years)} seasons; expected >100")
    return years


def _fetch_stats(group: str, level: str, season: int) -> list:
    """All season splits for one (group, level, season). Paginates on offset."""
    endpoint = "stats" if level == "player" else "teams/stats"
    out = []
    offset = 0
    while True:
        params = {
            "stats": "season",
            "group": group,
            "season": season,
            "sportId": 1,
            "limit": PAGE_LIMIT,
            "offset": offset,
        }
        if level == "player":
            params["playerPool"] = "all"
        blocks = _get_json(endpoint, params).get("stats", [])
        if not blocks:
            break
        splits = blocks[0].get("splits", []) or []
        total = blocks[0].get("totalSplits", 0) or 0
        out.extend(splits)
        offset += PAGE_LIMIT
        if not splits or offset >= total:
            break
        if offset > MAX_OFFSET:
            raise RuntimeError(f"{endpoint} {group} {season}: offset exceeded {MAX_OFFSET}")
    return out


# Stat fields published per group (source camelCase names, stored as strings in
# raw, TRY_CAST in SQL). Splitting count vs rate only governs the SQL cast type.
HITTING_COUNT = [
    "gamesPlayed", "plateAppearances", "atBats", "runs", "hits", "doubles",
    "triples", "homeRuns", "rbi", "baseOnBalls", "intentionalWalks", "strikeOuts",
    "stolenBases", "caughtStealing", "hitByPitch", "sacBunts", "sacFlies",
    "totalBases", "groundIntoDoublePlay",
]
HITTING_RATE = ["avg", "obp", "slg", "ops", "babip"]

PITCHING_COUNT = [
    "gamesPlayed", "gamesStarted", "gamesPitched", "wins", "losses", "saves",
    "saveOpportunities", "holds", "blownSaves", "hits", "runs", "earnedRuns",
    "homeRuns", "baseOnBalls", "intentionalWalks", "strikeOuts", "hitBatsmen",
    "wildPitches", "balks", "battersFaced", "completeGames", "shutouts",
]
PITCHING_RATE = ["era", "whip", "strikeoutsPer9Inn", "walksPer9Inn"]
PITCHING_STR = ["inningsPitched"]

FIELDING_COUNT = [
    "gamesPlayed", "gamesStarted", "assists", "putOuts", "errors", "chances",
    "doublePlays", "triplePlays",
]
FIELDING_RATE = ["fielding", "rangeFactorPerGame", "rangeFactorPer9Inn"]
FIELDING_STR = ["innings"]

GROUP_FIELDS = {
    "hitting": (HITTING_COUNT, HITTING_RATE, []),
    "pitching": (PITCHING_COUNT, PITCHING_RATE, PITCHING_STR),
    "fielding": (FIELDING_COUNT, FIELDING_RATE, FIELDING_STR),
}


def _stat_value(stat: dict, key: str):
    v = stat.get(key)
    return None if v is None else str(v)


def _flatten_player(split: dict, group: str, season: int) -> dict:
    stat = split.get("stat", {}) or {}
    player = split.get("player", {}) or {}
    team = split.get("team", {}) or {}
    league = split.get("league", {}) or {}
    pos = split.get("position", {}) or {}
    count, rate, strc = GROUP_FIELDS[group]
    row = {
        "season": season,
        "player_id": player.get("id"),
        "player_name": player.get("fullName"),
        "team_id": team.get("id"),
        "team_name": team.get("name"),
        "league_id": league.get("id"),
    }
    if group == "fielding":
        row["position_code"] = pos.get("code")
        row["position_name"] = pos.get("name")
        row["position_abbreviation"] = pos.get("abbreviation")
    for k in count + rate + strc:
        row[k] = _stat_value(stat, k)
    return row


def _flatten_team(split: dict, group: str, season: int) -> dict:
    stat = split.get("stat", {}) or {}
    team = split.get("team", {}) or {}
    count, rate, strc = GROUP_FIELDS[group]
    row = {
        "season": season,
        "team_id": team.get("id"),
        "team_name": team.get("name"),
    }
    for k in count + rate + strc:
        row[k] = _stat_value(stat, k)
    return row


def _fetch_stat_asset(node_id: str, group: str, level: str) -> None:
    asset = node_id
    flatten = _flatten_player if level == "player" else _flatten_team
    rows = []
    for season in _all_seasons():
        for split in _fetch_stats(group, level, season):
            rows.append(flatten(split, group, season))
    if not rows:
        raise RuntimeError(f"{asset}: no rows across any season")
    save_raw_ndjson(rows, asset)


# Concrete per-entity fetch fns (top-level, single param, no closures) ----------

def fetch_player_hitting(node_id: str) -> None:
    _fetch_stat_asset(node_id, "hitting", "player")


def fetch_player_pitching(node_id: str) -> None:
    _fetch_stat_asset(node_id, "pitching", "player")


def fetch_player_fielding(node_id: str) -> None:
    _fetch_stat_asset(node_id, "fielding", "player")


def fetch_team_hitting(node_id: str) -> None:
    _fetch_stat_asset(node_id, "hitting", "team")


def fetch_team_pitching(node_id: str) -> None:
    _fetch_stat_asset(node_id, "pitching", "team")


def fetch_team_fielding(node_id: str) -> None:
    _fetch_stat_asset(node_id, "fielding", "team")


def fetch_standings(node_id: str) -> None:
    asset = node_id
    rows = []
    for season in _all_seasons():
        data = _get_json("standings", {"leagueId": "103,104", "season": season})
        for rec in data.get("records", []) or []:
            league = rec.get("league", {}) or {}
            division = rec.get("division", {}) or {}
            for tr in rec.get("teamRecords", []) or []:
                team = tr.get("team", {}) or {}
                streak = tr.get("streak", {}) or {}
                rows.append({
                    "season": int(tr.get("season") or season),
                    "team_id": team.get("id"),
                    "team_name": team.get("name"),
                    "league_id": league.get("id"),
                    "division_id": division.get("id"),
                    "division_rank": _none_str(tr.get("divisionRank")),
                    "league_rank": _none_str(tr.get("leagueRank")),
                    "sport_rank": _none_str(tr.get("sportRank")),
                    "games_played": _none_str(tr.get("gamesPlayed")),
                    "wins": _none_str(tr.get("wins")),
                    "losses": _none_str(tr.get("losses")),
                    "winning_percentage": _none_str(tr.get("winningPercentage")),
                    "games_back": _none_str(tr.get("gamesBack")),
                    "runs_scored": _none_str(tr.get("runsScored")),
                    "runs_allowed": _none_str(tr.get("runsAllowed")),
                    "run_differential": _none_str(tr.get("runDifferential")),
                    "streak": streak.get("streakCode"),
                })
    if not rows:
        raise RuntimeError(f"{asset}: no standings rows across any season")
    save_raw_ndjson(rows, asset)


def _none_str(v):
    return None if v is None else str(v)


DOWNLOAD_SPECS = [
    NodeSpec(id="mlb-stats-api-standings", fn=fetch_standings, kind="download"),
    NodeSpec(id="mlb-stats-api-team-hitting", fn=fetch_team_hitting, kind="download"),
    NodeSpec(id="mlb-stats-api-team-pitching", fn=fetch_team_pitching, kind="download"),
    NodeSpec(id="mlb-stats-api-team-fielding", fn=fetch_team_fielding, kind="download"),
    NodeSpec(id="mlb-stats-api-player-hitting", fn=fetch_player_hitting, kind="download"),
    NodeSpec(id="mlb-stats-api-player-pitching", fn=fetch_player_pitching, kind="download"),
    NodeSpec(id="mlb-stats-api-player-fielding", fn=fetch_player_fielding, kind="download"),
]


# Transform SQL generation -----------------------------------------------------

def _q(name: str) -> str:
    return f'"{name}"'


def _stat_select(view: str, ident_exprs: list, group: str) -> str:
    count, rate, strc = GROUP_FIELDS[group]
    parts = list(ident_exprs)
    for c in count:
        parts.append(f"TRY_CAST({_q(c)} AS BIGINT) AS {_q(c)}")
    for c in rate:
        parts.append(f"TRY_CAST({_q(c)} AS DOUBLE) AS {_q(c)}")
    for c in strc:
        parts.append(f"CAST({_q(c)} AS VARCHAR) AS {_q(c)}")
    return f"SELECT\n  " + ",\n  ".join(parts) + f"\nFROM {_q(view)}\nWHERE season IS NOT NULL"


_PLAYER_IDENT = [
    "CAST(season AS INTEGER) AS season",
    "CAST(player_id AS BIGINT) AS player_id",
    "CAST(player_name AS VARCHAR) AS player_name",
    "CAST(team_id AS BIGINT) AS team_id",
    "CAST(team_name AS VARCHAR) AS team_name",
    "CAST(league_id AS BIGINT) AS league_id",
]
_PLAYER_FIELDING_IDENT = _PLAYER_IDENT + [
    "CAST(position_code AS VARCHAR) AS position_code",
    "CAST(position_name AS VARCHAR) AS position_name",
    "CAST(position_abbreviation AS VARCHAR) AS position_abbreviation",
]
_TEAM_IDENT = [
    "CAST(season AS INTEGER) AS season",
    "CAST(team_id AS BIGINT) AS team_id",
    "CAST(team_name AS VARCHAR) AS team_name",
]

_STANDINGS_SQL = f"""
SELECT
  CAST(season AS INTEGER) AS season,
  CAST(team_id AS BIGINT) AS team_id,
  CAST(team_name AS VARCHAR) AS team_name,
  CAST(league_id AS BIGINT) AS league_id,
  CAST(division_id AS BIGINT) AS division_id,
  TRY_CAST(division_rank AS INTEGER) AS division_rank,
  TRY_CAST(league_rank AS INTEGER) AS league_rank,
  TRY_CAST(sport_rank AS INTEGER) AS sport_rank,
  TRY_CAST(games_played AS INTEGER) AS games_played,
  TRY_CAST(wins AS INTEGER) AS wins,
  TRY_CAST(losses AS INTEGER) AS losses,
  TRY_CAST(winning_percentage AS DOUBLE) AS winning_percentage,
  CAST(games_back AS VARCHAR) AS games_back,
  TRY_CAST(runs_scored AS INTEGER) AS runs_scored,
  TRY_CAST(runs_allowed AS INTEGER) AS runs_allowed,
  TRY_CAST(run_differential AS INTEGER) AS run_differential,
  CAST(streak AS VARCHAR) AS streak
FROM "mlb-stats-api-standings"
WHERE season IS NOT NULL AND team_id IS NOT NULL
"""

_STAT_TRANSFORM = {
    "mlb-stats-api-team-hitting": (_TEAM_IDENT, "hitting"),
    "mlb-stats-api-team-pitching": (_TEAM_IDENT, "pitching"),
    "mlb-stats-api-team-fielding": (_TEAM_IDENT, "fielding"),
    "mlb-stats-api-player-hitting": (_PLAYER_IDENT, "hitting"),
    "mlb-stats-api-player-pitching": (_PLAYER_IDENT, "pitching"),
    "mlb-stats-api-player-fielding": (_PLAYER_FIELDING_IDENT, "fielding"),
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="mlb-stats-api-standings-transform",
        deps=["mlb-stats-api-standings"],
        sql=_STANDINGS_SQL,
    ),
] + [
    SqlNodeSpec(
        id=f"{download_id}-transform",
        deps=[download_id],
        sql=_stat_select(download_id, ident, group),
    )
    for download_id, (ident, group) in _STAT_TRANSFORM.items()
]
