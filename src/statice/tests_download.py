"""Post-download health checks for Statistics Iceland raw assets."""

from subsets_utils import list_raw_files, load_raw_ndjson


def test_every_asset_wrote_raw_ndjson(spec_ids):
    missing = [sid for sid in spec_ids if not list_raw_files(f"{sid}.ndjson*")]
    assert not missing, f"{len(missing)} specs wrote no raw ndjson, e.g. {missing[:5]}"


def test_sample_assets_nonempty_and_shaped(spec_ids):
    ordered = sorted(spec_ids)
    step = max(1, len(ordered) // 60)
    for sid in ordered[::step]:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"
        first = rows[0]
        assert "obs_value" in first, f"{sid}: first row missing obs_value"
        assert "_table_id" in first, f"{sid}: first row missing _table_id"
        assert "_source_updated" in first, f"{sid}: first row missing _source_updated"
