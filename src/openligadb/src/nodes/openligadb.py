"""OpenLigaDB connector — German community sports-results API.

Mechanism: public REST at https://api.openligadb.de (no auth). The league
catalog (`getavailableleagues`) enumerates ~800 league-seasons; every other
endpoint is keyed by (leagueShortcut, leagueSeason). We re-pull the full corpus
each run (stateless full snapshot — the whole source is a few thousand small
JSON responses, finishing in minutes) and overwrite.

Four published subsets, each a long-format table across all league-seasons:
  - matches     (one row per match)        from getmatchdata
  - goals       (one row per goal event)   from getmatchdata (nested goals)
  - standings   (one row per team-season)  from getbltable
  - goalgetters (one row per scorer-season) from getgoalgetters

matches and goals both read getmatchdata independently (download nodes are
independent); the redundant fetch is cheap on this unmetered API.
"""

from urllib.parse import quote

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)

BASE = "https://api.openligadb.de"


@transient_retry()
def _get_json(path):
    resp = get(f"{BASE}{path}", timeout=(10.0, 120.0), headers={"Accept": "application/json"})
    resp.raise_for_status()
    return resp.json()


def _seg(value):
    """URL-encode a single path segment. The community catalog contains junk
    shortcuts with spaces and even slashes (e.g. 'AK NM/J W'); without encoding
    those break path routing into a 404."""
    return quote(str(value), safe="")


def _get_league_json(endpoint, shortcut, season):
    """Fetch one league-season endpoint, tolerating a malformed/unknown entry.

    Valid leagues return 200 (an empty list when there's no data). A junk
    catalog entry yields a permanent 4xx — skip it per-league rather than
    failing the whole corpus node. 5xx/429 are retried upstream by
    transient_retry; an exhausted-retry 4xx still lands here and is skipped."""
    path = f"/{endpoint}/{_seg(shortcut)}/{_seg(season)}"
    try:
        return _get_json(path)
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        if 400 <= status < 500:
            print(f"[openligadb] skip {endpoint} {shortcut!r}/{season!r}: HTTP {status}")
            return []
        raise


def _league_seasons():
    """Unique (leagueShortcut, leagueSeason) pairs from the catalog.

    getmatchdata/getbltable/getgoalgetters are all keyed by shortcut+season, so
    that pair is the iteration unit. Distinct pairs (not leagueId) because the
    keyed endpoints resolve a shortcut+season to a single league internally.
    """
    leagues = _get_json("/getavailableleagues")
    pairs = {}
    for lg in leagues:
        sc = lg.get("leagueShortcut")
        season = lg.get("leagueSeason")
        if not sc or season is None:
            continue
        pairs[(sc, str(season))] = True
    return sorted(pairs.keys())


def _extract_results(match_results):
    """Pull (halftime, full-time) scores out of a match's matchResults list.

    resultTypeID is NOT a reliable discriminator: the full-time score is type 2
    in the modern Bundesliga but type 0 (and frequently the only entry) across
    most other leagues. The stable signal is resultName ('Endergebnis' = final,
    'Halbzeitergebnis' = halftime). Fallback for the final: the highest
    resultOrderID is the last/most-complete recorded score."""
    results = match_results or []
    ht1 = ht2 = ft1 = ft2 = None
    final = None
    for r in results:
        name = r.get("resultName") or ""
        if "Halbzeit" in name:
            ht1, ht2 = r.get("pointsTeam1"), r.get("pointsTeam2")
        if "Endergebnis" in name:
            final = r
    if final is None and results:
        final = max(results, key=lambda r: r.get("resultOrderID") or 0)
    if final is not None:
        ft1, ft2 = final.get("pointsTeam1"), final.get("pointsTeam2")
    return ht1, ht2, ft1, ft2


def _season_int(value, fallback):
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(fallback)
        except (TypeError, ValueError):
            return None


def fetch_matches(node_id: str) -> None:
    asset = node_id
    rows = []
    for shortcut, season in _league_seasons():
        matches = _get_league_json("getmatchdata", shortcut, season)
        if not matches:
            continue
        for m in matches:
            ht1, ht2, ft1, ft2 = _extract_results(m.get("matchResults"))
            group = m.get("group") or {}
            team1 = m.get("team1") or {}
            team2 = m.get("team2") or {}
            loc = m.get("location") or {}
            rows.append({
                "match_id": m.get("matchID"),
                "league_id": m.get("leagueId"),
                "league_name": m.get("leagueName"),
                "league_shortcut": shortcut,
                "league_season": _season_int(m.get("leagueSeason"), season),
                "matchday": group.get("groupOrderID"),
                "matchday_name": group.get("groupName"),
                "match_datetime_utc": m.get("matchDateTimeUTC"),
                "match_is_finished": m.get("matchIsFinished"),
                "last_update": m.get("lastUpdateDateTime"),
                "team1_id": team1.get("teamId"),
                "team1_name": team1.get("teamName"),
                "team2_id": team2.get("teamId"),
                "team2_name": team2.get("teamName"),
                "halftime_team1": ht1,
                "halftime_team2": ht2,
                "final_team1": ft1,
                "final_team2": ft2,
                "location_id": loc.get("locationID"),
                "location_city": loc.get("locationCity"),
                "location_stadium": loc.get("locationStadium"),
                "number_of_viewers": m.get("numberOfViewers"),
            })
    save_raw_ndjson(rows, asset)


def fetch_goals(node_id: str) -> None:
    asset = node_id
    rows = []
    for shortcut, season in _league_seasons():
        matches = _get_league_json("getmatchdata", shortcut, season)
        if not matches:
            continue
        for m in matches:
            match_id = m.get("matchID")
            season_int = _season_int(m.get("leagueSeason"), season)
            for g in m.get("goals") or []:
                rows.append({
                    "goal_id": g.get("goalID"),
                    "match_id": match_id,
                    "league_shortcut": shortcut,
                    "league_season": season_int,
                    "score_team1": g.get("scoreTeam1"),
                    "score_team2": g.get("scoreTeam2"),
                    "match_minute": g.get("matchMinute"),
                    "goal_getter_id": g.get("goalGetterID"),
                    "goal_getter_name": g.get("goalGetterName"),
                    "is_penalty": g.get("isPenalty"),
                    "is_own_goal": g.get("isOwnGoal"),
                    "is_overtime": g.get("isOvertime"),
                    "comment": g.get("comment"),
                })
    save_raw_ndjson(rows, asset)


def fetch_standings(node_id: str) -> None:
    asset = node_id
    rows = []
    for shortcut, season in _league_seasons():
        table = _get_league_json("getbltable", shortcut, season)
        if not table:
            continue
        season_int = _season_int(season, season)
        for t in table:
            rows.append({
                "league_shortcut": shortcut,
                "league_season": season_int,
                "team_id": t.get("teamInfoId"),
                "team_name": t.get("teamName"),
                "short_name": t.get("shortName"),
                "points": t.get("points"),
                "matches": t.get("matches"),
                "won": t.get("won"),
                "draw": t.get("draw"),
                "lost": t.get("lost"),
                "goals": t.get("goals"),
                "opponent_goals": t.get("opponentGoals"),
                "goal_diff": t.get("goalDiff"),
            })
    save_raw_ndjson(rows, asset)


def fetch_goalgetters(node_id: str) -> None:
    asset = node_id
    rows = []
    for shortcut, season in _league_seasons():
        scorers = _get_league_json("getgoalgetters", shortcut, season)
        if not scorers:
            continue
        season_int = _season_int(season, season)
        for s in scorers:
            rows.append({
                "league_shortcut": shortcut,
                "league_season": season_int,
                "goal_getter_id": s.get("goalGetterId"),
                "goal_getter_name": s.get("goalGetterName"),
                "goal_count": s.get("goalCount"),
            })
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="openligadb-matches", fn=fetch_matches, kind="download"),
    NodeSpec(id="openligadb-goals", fn=fetch_goals, kind="download"),
    NodeSpec(id="openligadb-standings", fn=fetch_standings, kind="download"),
    NodeSpec(id="openligadb-goalgetters", fn=fetch_goalgetters, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openligadb-matches-transform",
        deps=["openligadb-matches"],
        key=("match_id",),
        temporal="match_datetime_utc",
        sql='''
            SELECT
                CAST(match_id AS BIGINT)             AS match_id,
                league_shortcut,
                CAST(league_season AS INTEGER)       AS league_season,
                CAST(league_id AS BIGINT)            AS league_id,
                league_name,
                CAST(matchday AS INTEGER)            AS matchday,
                matchday_name,
                CAST(match_datetime_utc AS TIMESTAMP) AS match_datetime_utc,
                CAST(match_is_finished AS BOOLEAN)   AS match_is_finished,
                CAST(team1_id AS BIGINT)             AS team1_id,
                team1_name,
                CAST(team2_id AS BIGINT)             AS team2_id,
                team2_name,
                CAST(halftime_team1 AS INTEGER)      AS halftime_team1,
                CAST(halftime_team2 AS INTEGER)      AS halftime_team2,
                CAST(final_team1 AS INTEGER)         AS final_team1,
                CAST(final_team2 AS INTEGER)         AS final_team2,
                location_city,
                location_stadium,
                CAST(number_of_viewers AS BIGINT)    AS number_of_viewers
            FROM "openligadb-matches"
            WHERE match_id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY match_id ORDER BY last_update DESC NULLS LAST) = 1
        ''',
    ),
    SqlNodeSpec(
        id="openligadb-goals-transform",
        deps=["openligadb-goals"],
        key=("goal_id",),
        temporal="league_season",
        sql='''
            SELECT
                CAST(goal_id AS BIGINT)        AS goal_id,
                CAST(match_id AS BIGINT)       AS match_id,
                league_shortcut,
                CAST(league_season AS INTEGER) AS league_season,
                CAST(score_team1 AS INTEGER)   AS score_team1,
                CAST(score_team2 AS INTEGER)   AS score_team2,
                CAST(match_minute AS INTEGER)  AS match_minute,
                CAST(goal_getter_id AS BIGINT) AS goal_getter_id,
                goal_getter_name,
                CAST(is_penalty AS BOOLEAN)    AS is_penalty,
                CAST(is_own_goal AS BOOLEAN)   AS is_own_goal,
                CAST(is_overtime AS BOOLEAN)   AS is_overtime,
                comment
            FROM "openligadb-goals"
            WHERE goal_id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY goal_id ORDER BY goal_id) = 1
        ''',
    ),
    SqlNodeSpec(
        id="openligadb-standings-transform",
        deps=["openligadb-standings"],
        key=("league_shortcut", "league_season", "team_id"),
        temporal="league_season",
        sql='''
            SELECT
                league_shortcut,
                CAST(league_season AS INTEGER) AS league_season,
                CAST(team_id AS BIGINT)        AS team_id,
                team_name,
                short_name,
                CAST(points AS INTEGER)        AS points,
                CAST(matches AS INTEGER)       AS matches,
                CAST(won AS INTEGER)           AS won,
                CAST(draw AS INTEGER)          AS draw,
                CAST(lost AS INTEGER)          AS lost,
                CAST(goals AS INTEGER)         AS goals,
                CAST(opponent_goals AS INTEGER) AS opponent_goals,
                CAST(goal_diff AS INTEGER)     AS goal_diff
            FROM "openligadb-standings"
            WHERE team_id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY league_shortcut, league_season, team_id ORDER BY points DESC) = 1
        ''',
    ),
    SqlNodeSpec(
        id="openligadb-goalgetters-transform",
        deps=["openligadb-goalgetters"],
        key=("league_shortcut", "league_season", "goal_getter_id"),
        temporal="league_season",
        sql='''
            SELECT
                league_shortcut,
                CAST(league_season AS INTEGER) AS league_season,
                CAST(goal_getter_id AS BIGINT) AS goal_getter_id,
                goal_getter_name,
                CAST(goal_count AS INTEGER)    AS goal_count
            FROM "openligadb-goalgetters"
            WHERE goal_getter_id IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY league_shortcut, league_season, goal_getter_id ORDER BY goal_count DESC) = 1
        ''',
    ),
]
