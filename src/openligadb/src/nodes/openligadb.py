"""OpenLigaDB connector — German community sports-results API.

Mechanism: public REST at https://api.openligadb.de (no auth). The league
catalog (`getavailableleagues`) enumerates ~800 league-seasons; every other
endpoint is keyed by (leagueShortcut, leagueSeason). We re-pull the full corpus
each run (stateless full snapshot — the whole source is a few thousand small
JSON responses, finishing in minutes) and overwrite.

Six published subsets, each a long-format table across all league-seasons:
  - leagues     (one row per league-season) from getavailableleagues
  - teams       (one row per team-season)    from getavailableteams
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
    get,
    save_raw_ndjson,
)

BASE = "https://api.openligadb.de"


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


def fetch_leagues(node_id: str) -> None:
    rows = []
    for lg in _get_json("/getavailableleagues"):
        sport = lg.get("sport") or {}
        rows.append({
            "league_id": lg.get("leagueId"),
            "league_name": lg.get("leagueName"),
            "league_shortcut": lg.get("leagueShortcut"),
            "league_season": _season_int(lg.get("leagueSeason"), lg.get("leagueSeason")),
            "sport_id": sport.get("sportId"),
            "sport_name": sport.get("sportName"),
        })
    save_raw_ndjson(rows, node_id)


def fetch_teams(node_id: str) -> None:
    rows = []
    for shortcut, season in _league_seasons():
        teams = _get_league_json("getavailableteams", shortcut, season)
        if not teams:
            continue
        season_int = _season_int(season, season)
        for t in teams:
            rows.append({
                "league_shortcut": shortcut,
                "league_season": season_int,
                "team_id": t.get("teamId"),
                "team_name": t.get("teamName"),
                "short_name": t.get("shortName"),
                "team_icon_url": t.get("teamIconUrl"),
                "team_group_name": t.get("teamGroupName"),
            })
    save_raw_ndjson(rows, node_id)


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
    NodeSpec(id="openligadb-leagues", fn=fetch_leagues, kind="download"),
    NodeSpec(id="openligadb-teams", fn=fetch_teams, kind="download"),
    NodeSpec(id="openligadb-matches", fn=fetch_matches, kind="download"),
    NodeSpec(id="openligadb-goals", fn=fetch_goals, kind="download"),
    NodeSpec(id="openligadb-standings", fn=fetch_standings, kind="download"),
    NodeSpec(id="openligadb-goalgetters", fn=fetch_goalgetters, kind="download"),
]
