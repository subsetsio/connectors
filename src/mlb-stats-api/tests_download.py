"""Health-invariant tests for the MLB Stats API connector.

Run post-DAG in-connector against the raw NDJSON assets each download node
saved. They catch silent degradation that file-existence alone misses: empty
payloads, single-season pulls (the season loop broke), missing identity keys.
"""

from subsets_utils import load_raw_ndjson


def test_all_assets_nonempty(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_season_spans_history(spec_ids):
    """Every asset must span many seasons — if the /seasons/all loop silently
    pulled one year, distinct seasons collapses to 1."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        seasons = {r.get("season") for r in rows if r.get("season") is not None}
        assert len(seasons) >= 50, f"{sid}: only {len(seasons)} distinct seasons"
        assert min(seasons) <= 1920, f"{sid}: earliest season {min(seasons)} > 1920"


def test_identity_keys_present(spec_ids):
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        assert sample.get("season") is not None, f"{sid}: null season in first row"
        assert sample.get("team_id") is not None, f"{sid}: null team_id in first row"
        if "player" in sid:
            assert sample.get("player_id") is not None, f"{sid}: null player_id"
