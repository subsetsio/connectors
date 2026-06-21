"""Health-invariant tests for the chicago-fed raw assets.

Run post-DAG inside the connector. They catch silent degradation that file
existence alone misses — empty payloads, a column schema collapse, dates that
stopped parsing, or a CSV that lost its history.
"""

from subsets_utils import load_raw_parquet

# Minimum row counts grounded in observed history (well below current counts so
# normal growth never trips them, high enough that a truncated/empty download does).
_MIN_ROWS = {
    "chicago-fed-nfci": 2500,   # weekly since 1971 (~2887 observed)
    "chicago-fed-cfnai": 650,   # monthly since 1967 (~710 observed)
    "chicago-fed-mei": 500,     # monthly 1976-2021, discontinued (~540 observed)
    "chicago-fed-bbki": 700,    # monthly since 1960, discontinued (~749 observed)
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset must hold rows. Empty usually means the endpoint
    switched format, moved, or the UA got blocked."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_row_counts_plausible(spec_ids):
    """Each product has a long history; a sharp shortfall means a truncated
    download or a parser that silently dropped most rows."""
    for sid in spec_ids:
        floor = _MIN_ROWS.get(sid)
        if floor is None:
            continue
        n = len(load_raw_parquet(sid))
        assert n >= floor, f"{sid}: got {n} rows, expected >= {floor}"


def test_date_and_index_columns(spec_ids):
    """Every product must carry a non-null 'date' column plus at least one
    numeric index column, and dates must be unique (one row per period)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        names = table.column_names
        assert "date" in names, f"{sid}: missing 'date' column (got {names})"
        assert len(names) >= 2, f"{sid}: no index columns beyond date ({names})"

        dates = table.column("date").to_pylist()
        assert all(d is not None for d in dates), f"{sid}: null dates present"
        assert len(dates) == len(set(dates)), f"{sid}: duplicate dates"
