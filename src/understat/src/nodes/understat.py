"""Understat connector downloads.

Understat exposes public JSON endpoints used by its own pages. There is no
published API contract, no incremental query support, and robots.txt disallows
automated crawling; that risk is recorded in the research asset. These downloads
therefore perform stateless full refreshes from the site JSON endpoints.
"""

from __future__ import annotations

from datetime import date
from time import sleep
from urllib.parse import quote

import httpx

from subsets_utils import NodeSpec, get, load_raw_ndjson, save_raw_ndjson

BASE_URL = "https://understat.com"
LEAGUES = {
    "EPL": "EPL",
    "La liga": "La_liga",
    "Bundesliga": "Bundesliga",
    "Serie A": "Serie_A",
    "Ligue 1": "Ligue_1",
    "RFPL": "RFPL",
}
FIRST_SEASON = 2014


def _latest_started_season() -> int:
    today = date.today()
    return today.year if today.month >= 8 else today.year - 1


def _seasons() -> range:
    return range(FIRST_SEASON, _latest_started_season() + 1)


def _headers(referer: str) -> dict[str, str]:
    return {
        "X-Requested-With": "XMLHttpRequest",
        "Referer": referer,
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }


def _get_json(path: str, referer: str) -> dict:
    resp = get(f"{BASE_URL}/{path}", headers=_headers(referer), timeout=(10.0, 120.0))
    resp.raise_for_status()
    sleep(0.2)
    return resp.json()


def _league_data(league: str, season: int) -> dict:
    encoded = quote(league)
    referer = f"{BASE_URL}/league/{LEAGUES[league]}/{season}"
    return _get_json(f"getLeagueData/{encoded}/{season}", referer)


def _match_data(match_id: str | int) -> dict:
    referer = f"{BASE_URL}/match/{match_id}"
    return _get_json(f"getMatchData/{match_id}", referer)


def _league_rows() -> list[dict]:
    return [
        {
            "league": league,
            "league_slug": slug,
            "season": season,
            "season_label": f"{season}/{season + 1}",
        }
        for league, slug in LEAGUES.items()
        for season in _seasons()
    ]


def _iter_league_payloads():
    for league in LEAGUES:
        for season in _seasons():
            payload = _league_data(league, season)
            # Future or unsupported league-season combinations may be empty near
            # a season boundary; historical seasons should not disappear.
            if not payload.get("teams") and not payload.get("dates"):
                if season < _latest_started_season():
                    raise RuntimeError(f"{league} {season}: empty historical league payload")
                continue
            yield league, season, payload


def _iter_match_ids() -> list[dict]:
    seen: set[str] = set()
    rows: list[dict] = []
    for league, season, payload in _iter_league_payloads():
        for match in payload.get("dates", []):
            match_id = str(match.get("id") or "")
            if not match_id or match_id in seen:
                continue
            seen.add(match_id)
            rows.append({"league": league, "season": season, "match_id": match_id})
    return rows


def fetch_leagues(node_id: str) -> None:
    save_raw_ndjson(_league_rows(), node_id)


def fetch_teams(node_id: str) -> None:
    rows: list[dict] = []
    for league, season, payload in _iter_league_payloads():
        for team_id, team in payload.get("teams", {}).items():
            rows.append(
                {
                    "league": league,
                    "season": season,
                    "team_id": str(team.get("id") or team_id),
                    "team_title": team.get("title"),
                }
            )
    if not rows:
        raise RuntimeError(f"{node_id}: no teams collected")
    save_raw_ndjson(rows, node_id)


def fetch_players(node_id: str) -> None:
    rows: list[dict] = []
    for league, season, payload in _iter_league_payloads():
        for player in payload.get("players", []):
            row = dict(player)
            row["league"] = league
            row["season"] = season
            rows.append(row)
    if not rows:
        raise RuntimeError(f"{node_id}: no players collected")
    save_raw_ndjson(rows, node_id)


def fetch_matches(node_id: str) -> None:
    rows: list[dict] = []
    for league, season, payload in _iter_league_payloads():
        for match in payload.get("dates", []):
            row = dict(match)
            row["league"] = league
            row["season"] = season
            rows.append(row)
    if not rows:
        raise RuntimeError(f"{node_id}: no matches collected")
    save_raw_ndjson(rows, node_id)


def fetch_team_match_stats(node_id: str) -> None:
    rows: list[dict] = []
    for league, season, payload in _iter_league_payloads():
        for team_id, team in payload.get("teams", {}).items():
            for idx, history in enumerate(team.get("history", []), start=1):
                row = dict(history)
                row["league"] = league
                row["season"] = season
                row["team_id"] = str(team.get("id") or team_id)
                row["team_title"] = team.get("title")
                row["match_index"] = idx
                rows.append(row)
    if not rows:
        raise RuntimeError(f"{node_id}: no team match stats collected")
    save_raw_ndjson(rows, node_id)


def _iter_match_payloads():
    for match in _iter_match_ids():
        try:
            payload = _match_data(match["match_id"])
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                continue
            raise
        yield match, payload


def _iter_roster_players(roster):
    if isinstance(roster, dict):
        yield from roster.items()
        return
    if isinstance(roster, list):
        for idx, player in enumerate(roster):
            yield str(idx), player


def fetch_shots(node_id: str) -> None:
    rows: list[dict] = []
    for match, payload in _iter_match_payloads():
        for side, shots in (payload.get("shots") or {}).items():
            for shot in shots:
                row = dict(shot)
                row.update(match)
                row["side"] = side
                rows.append(row)
    if not rows:
        raise RuntimeError(f"{node_id}: no shots collected")
    save_raw_ndjson(rows, node_id)


def fetch_rosters(node_id: str) -> None:
    rows: list[dict] = []
    for match, payload in _iter_match_payloads():
        for side, roster in (payload.get("rosters") or {}).items():
            for roster_id, player in _iter_roster_players(roster):
                row = dict(player)
                row.update(match)
                row["side"] = side
                row["roster_id"] = str(player.get("id") or roster_id)
                rows.append(row)
    if not rows:
        raise RuntimeError(f"{node_id}: no rosters collected")
    save_raw_ndjson(rows, node_id)


def fetch_player_match_stats(node_id: str) -> None:
    rows: list[dict] = []
    stat_cols = {
        "goals",
        "own_goals",
        "shots",
        "xG",
        "time",
        "player_id",
        "team_id",
        "position",
        "player",
        "h_a",
        "yellow_card",
        "red_card",
        "key_passes",
        "assists",
        "xA",
        "xGChain",
        "xGBuildup",
        "positionOrder",
    }
    for player in load_raw_ndjson("understat-rosters"):
        row = {col: player.get(col) for col in stat_cols}
        for col in ("league", "season", "match_id", "side", "roster_id"):
            row[col] = player.get(col)
        rows.append(row)
    if not rows:
        raise RuntimeError(f"{node_id}: no player match stats collected")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="understat-leagues", fn=fetch_leagues, kind="download"),
    NodeSpec(id="understat-teams", fn=fetch_teams, kind="download"),
    NodeSpec(id="understat-players", fn=fetch_players, kind="download"),
    NodeSpec(id="understat-matches", fn=fetch_matches, kind="download"),
    NodeSpec(id="understat-team-match-stats", fn=fetch_team_match_stats, kind="download"),
    NodeSpec(id="understat-shots", fn=fetch_shots, kind="download"),
    NodeSpec(id="understat-rosters", fn=fetch_rosters, kind="download"),
    NodeSpec(
        id="understat-player-match-stats",
        fn=fetch_player_match_stats,
        kind="download",
        deps=("understat-rosters",),
    ),
]
