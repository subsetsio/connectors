"""Health invariants for the Climate Action Tracker raw downloads."""

from subsets_utils import load_raw_parquet

# Expected record counts as observed at authoring time. The corpora are small
# and full-pulled each run; a large shortfall signals a truncated crawl or a
# silently-changed endpoint, not normal growth.
_MIN_ROWS = {
    "climate-action-tracker-country-emissions": 7000,
    "climate-action-tracker-sector-indicators": 6000,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_row_counts(spec_ids):
    """Each corpus should be roughly its known size — guards truncated crawls."""
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        table = load_raw_parquet(sid)
        assert len(table) >= floor, (
            f"{sid}: only {len(table)} rows, expected >= {floor} "
            "(possible truncated pagination)"
        )


def test_value_column_has_data(spec_ids):
    """The `value` column must carry real numbers, not be all-null."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("value")
        non_null = len(col) - col.null_count
        assert non_null > 0, f"{sid}: `value` column is entirely null"
