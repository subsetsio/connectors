import json, tempfile, os, duckdb
import sys
sys.path.insert(0, "src")
import nodes.mlb_stats_api as m

# small sample: 2 seasons of team-hitting + player-fielding + standings
def sample_stats(group, level, seasons):
    flat = m._flatten_player if level == "player" else m._flatten_team
    rows = []
    for s in seasons:
        for sp in m._fetch_stats(group, level, s):
            rows.append(flat(sp, group, s))
    return rows

def standings_rows(seasons):
    rows = []
    for s in seasons:
        data = m._get_json("standings", {"leagueId": "103,104", "season": s})
        for rec in data.get("records", []):
            league = rec.get("league", {}); division = rec.get("division", {})
            for tr in rec.get("teamRecords", []):
                team = tr.get("team", {}); streak = tr.get("streak", {}) or {}
                rows.append({
                    "season": int(tr.get("season") or s), "team_id": team.get("id"),
                    "team_name": team.get("name"), "league_id": league.get("id"),
                    "division_id": division.get("id"),
                    "division_rank": m._none_str(tr.get("divisionRank")),
                    "league_rank": m._none_str(tr.get("leagueRank")),
                    "sport_rank": m._none_str(tr.get("sportRank")),
                    "games_played": m._none_str(tr.get("gamesPlayed")),
                    "wins": m._none_str(tr.get("wins")), "losses": m._none_str(tr.get("losses")),
                    "winning_percentage": m._none_str(tr.get("winningPercentage")),
                    "games_back": m._none_str(tr.get("gamesBack")),
                    "runs_scored": m._none_str(tr.get("runsScored")),
                    "runs_allowed": m._none_str(tr.get("runsAllowed")),
                    "run_differential": m._none_str(tr.get("runDifferential")),
                    "streak": streak.get("streakCode"),
                })
    return rows

cases = {
    "mlb-stats-api-team-hitting": (sample_stats("hitting", "team", [1901, 2024]), m._stat_select("mlb-stats-api-team-hitting", m._TEAM_IDENT, "hitting")),
    "mlb-stats-api-player-pitching": (sample_stats("pitching", "player", [2024]), m._stat_select("mlb-stats-api-player-pitching", m._PLAYER_IDENT, "pitching")),
    "mlb-stats-api-player-fielding": (sample_stats("fielding", "player", [2024]), m._stat_select("mlb-stats-api-player-fielding", m._PLAYER_FIELDING_IDENT, "fielding")),
    "mlb-stats-api-standings": (standings_rows([1901, 2024]), m._STANDINGS_SQL),
}

con = duckdb.connect()
for asset, (rows, sql) in cases.items():
    f = os.path.join(tempfile.gettempdir(), asset + ".ndjson")
    with open(f, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    con.execute(f'CREATE OR REPLACE VIEW "{asset}" AS SELECT * FROM read_json_auto(?)', [f])
    out = con.execute(sql).arrow()
    print(f"\n=== {asset}: raw={len(rows)} -> published rows={out.num_rows} cols={out.num_columns}")
    print("schema:", {c.name: str(c.type) for c in out.schema}.__repr__()[:400])
    # show a couple rows of a few columns
    print(out.slice(0, 2).to_pydict().get("season"), "sample season values")
