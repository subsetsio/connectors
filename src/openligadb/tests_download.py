"""Health-invariant tests for OpenLigaDB raw assets.

Catch silent degradation the file-existence check misses: empty payloads,
truncated catalog crawls, or a key going missing because the response shape
changed. Loaded through the same subsets_utils loader the download used
(save_raw_ndjson -> load_raw_ndjson).
"""

from subsets_utils import load_raw_ndjson

EXPECTED_KEYS = {
    "openligadb-matches": {"match_id", "league_shortcut", "league_season", "final_team1"},
    "openligadb-goals": {"goal_id", "match_id", "league_shortcut", "goal_getter_name"},
    "openligadb-standings": {"team_id", "league_shortcut", "league_season", "points"},
    "openligadb-goalgetters": {"goal_getter_id", "league_shortcut", "goal_count"},
}

# Loose floors: matches/goals are large; standings/goalgetters smaller. A crawl
# that broke after the first league-season would fall far below these.
MIN_ROWS = {
    "openligadb-matches": 20000,
    "openligadb-goals": 10000,
    "openligadb-standings": 2000,
    "openligadb-goalgetters": 2000,
}


def test_raw_assets_nonempty_and_shaped(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"
        floor = MIN_ROWS.get(sid, 1)
        assert len(rows) >= floor, f"{sid}: only {len(rows)} rows; expected >= {floor}"
        keys = EXPECTED_KEYS.get(sid, set())
        missing = keys - set(rows[0].keys())
        assert not missing, f"{sid}: first row missing expected keys {missing}"
