"""Post-DAG health invariants for the Kenneth French Data Library raw assets.

These run in-connector after the download nodes, loading raw through the same
loader the fetch fn wrote with. They catch silent degradation that file
existence alone misses: empty/truncated downloads, a parser that stopped
emitting values, or a format change that collapsed the long table.
"""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {"block", "statistic", "period", "date", "variable", "value"}
VALID_PERIODS = {"annual", "monthly", "weekly", "daily"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset must parse to a non-empty long table. Zero rows means the
    ZIP was empty/truncated or the stacked-table parser failed to find data."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_and_periods(spec_ids):
    """Long-format schema is stable and every period token is one we emit."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert EXPECTED_COLS <= cols, f"{sid}: missing columns {EXPECTED_COLS - cols}"
        periods = set(table.column("period").to_pylist())
        bad = periods - VALID_PERIODS
        assert not bad, f"{sid}: unexpected period values {bad}"


def test_values_are_real(spec_ids):
    """No surviving sentinel values, and at least one finite observation per
    dataset (the parser drops -99.99/-999 before writing)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("value").to_pylist()
        assert any(v is not None for v in vals), f"{sid}: no non-null values"
        leaked = [v for v in vals if v is not None and (abs(v + 99.99) < 1e-6 or abs(v + 999.0) < 1e-6)]
        assert not leaked, f"{sid}: {len(leaked)} sentinel values leaked into raw"
