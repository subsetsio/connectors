"""Health invariants for the QoG bulk-CSV downloads.

Each raw asset is the full parsed CSV for one QoG dataset. The checks catch the
silent-degradation modes file existence misses: an empty/truncated download, a
table that collapsed to a single ID column, or a wide compilation dataset that
arrived far narrower than its known shape (a sign the file or format changed).
"""
from subsets_utils import load_raw_parquet

# Floor on column count for the wide compilation datasets — they carry hundreds
# to ~2100 variables. A collapse below this means the CSV changed shape.
_MIN_COLS = {
    "quality-of-government-qog-std-ts": 1000,
    "quality-of-government-qog-std-cs": 1000,
    "quality-of-government-qog-bas-ts": 200,
    "quality-of-government-qog-bas-cs": 200,
    "quality-of-government-qog-oecd-ts": 500,
    "quality-of-government-qog-oecd-cs": 500,
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download's raw parquet must hold rows and more than one column."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"
        assert table.num_columns > 1, (
            f"{sid}: only {table.num_columns} column(s) — table collapsed"
        )


def test_wide_datasets_kept_width(spec_ids):
    """The compilation datasets are wide; a sharp narrowing means the upstream
    file or CSV format changed and we silently lost variables."""
    for sid in spec_ids:
        floor = _MIN_COLS.get(sid)
        if floor is None:
            continue
        table = load_raw_parquet(sid)
        assert table.num_columns >= floor, (
            f"{sid}: {table.num_columns} columns, expected >= {floor}"
        )
