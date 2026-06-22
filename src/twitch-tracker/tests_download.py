"""Health-invariant tests for the TwitchTracker connector.

Run post-DAG inside the connector. They load raw via the same subsets_utils
loader the fetch fns used (save_raw_parquet -> load_raw_parquet) and catch
silent degradation that file existence alone misses: empty payloads, missing
columns, or a row where every metric is null (the summary endpoint started
returning empty objects for everything).
"""

from subsets_utils import load_raw_parquet

_EXPECTED_COLUMNS = {
    "twitch-tracker-channels": {
        "channel", "rank", "minutes_streamed", "avg_viewers", "max_viewers",
        "hours_watched", "followers", "followers_total", "captured_date",
    },
    "twitch-tracker-games": {
        "game", "rank", "avg_viewers", "avg_channels", "hours_watched",
        "captured_date",
    },
}


def test_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows. An empty snapshot means the
    summary endpoint returned `{}` for every seed (rate-limited or changed)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_raw_assets_have_expected_columns(spec_ids):
    """Guard against the response schema drifting under us."""
    for sid in spec_ids:
        expected = _EXPECTED_COLUMNS.get(sid)
        if expected is None:
            continue
        cols = set(load_raw_parquet(sid).column_names)
        missing = expected - cols
        assert not missing, f"{sid}: missing expected columns {sorted(missing)}"


def test_metrics_not_all_null(spec_ids):
    """At least some rows must carry a non-null rank — if every rank is null
    the endpoint is returning empty objects that slipped past the skip guard."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if "rank" not in table.column_names:
            continue
        non_null = table.column("rank").null_count
        assert non_null < len(table), f"{sid}: every rank is null"
