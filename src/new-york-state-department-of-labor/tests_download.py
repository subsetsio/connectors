from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset's per-entity SODA endpoint returns the full table; an empty
    payload means pagination broke after page 1 or the dataset id went stale."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_rows_are_flat(spec_ids):
    """The fetch fn flattens nested Socrata objects to JSON strings, so no raw
    value should still be a dict/list — if one is, the flatten step regressed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        for row in rows[:200]:
            bad = [k for k, v in row.items() if isinstance(v, (dict, list))]
            assert not bad, f"{sid}: nested (unflattened) columns {bad}"
