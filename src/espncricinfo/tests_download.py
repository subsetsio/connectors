"""Post-DAG health invariants for the ESPNcricinfo raw assets.

All raw assets are written with save_raw_ndjson, so we read them back with
load_raw_ndjson and assert the payloads are non-empty and structurally sane —
catching silent degradation (endpoint format flips, auth/challenge walls,
truncated crawls) that mere file-existence checks miss.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw ndjson must hold at least one record."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_scorecard_rows_have_player_ids(spec_ids):
    """Batting/bowling lines must be keyed to a player — a roster shape change
    would silently drop player ids."""
    for sid in ("espncricinfo-batting-innings", "espncricinfo-bowling-innings"):
        if sid not in spec_ids:
            continue
        rows = load_raw_ndjson(sid)
        missing = [r for r in rows if not r.get("player_id")]
        assert not missing, f"{sid}: {len(missing)} scorecard rows missing player_id"


def test_statsguru_spans_multiple_classes(spec_ids):
    """Statsguru aggregates are pulled per match class (Test/ODI/T20I). If only
    one class came back the per-class crawl partially failed."""
    for sid in spec_ids:
        if "statsguru" not in sid:
            continue
        rows = load_raw_ndjson(sid)
        classes = {r.get("match_class") for r in rows}
        assert "Test" in classes, f"{sid}: no Test-class records ({classes})"
        assert len(classes) >= 2, f"{sid}: only one match class present ({classes})"
