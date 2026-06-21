"""Post-DAG health invariants for the SteamDB connector raw assets."""
from subsets_utils import load_raw_parquet

_CHART_SPECS = {"steamdb-concurrent-players", "steamdb-most-played"}
_ENRICH_SPECS = {"steamdb-app-details", "steamdb-app-reviews"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must land rows. Empty = endpoint changed shape or
    the store host silently throttled to null bodies."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_charts_full(spec_ids):
    """The concurrent/most-played leaderboards return ~100 ranks; <50 means a
    truncated payload slipped past the fetch."""
    for sid in spec_ids:
        if sid in _CHART_SPECS:
            n = len(load_raw_parquet(sid))
            assert n >= 50, f"{sid}: only {n} ranks, expected ~100"


def test_appid_universe_enriched(spec_ids):
    """Enrichment tables should cover most of the ~200-app chart universe and
    carry valid positive appids; a collapse signals store throttling."""
    for sid in spec_ids:
        if sid in _ENRICH_SPECS:
            table = load_raw_parquet(sid)
            assert len(table) >= 50, f"{sid}: only {len(table)} apps enriched, expected >=50"
            appids = table.column("appid").to_pylist()
            assert all(a and a > 0 for a in appids), f"{sid}: non-positive appid present"


def test_reviews_totals_consistent(spec_ids):
    """total_reviews should equal positive+negative for review summaries."""
    if "steamdb-app-reviews" not in spec_ids:
        return
    t = load_raw_parquet("steamdb-app-reviews")
    pos = t.column("total_positive").to_pylist()
    neg = t.column("total_negative").to_pylist()
    tot = t.column("total_reviews").to_pylist()
    bad = [i for i in range(len(tot)) if (pos[i] + neg[i]) != tot[i]]
    assert not bad, f"app-reviews: {len(bad)} rows where positive+negative != total"
