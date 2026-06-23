"""Health-invariant tests for GFED raw assets, run post-DAG in-connector."""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {"species", "fire_type", "region", "year", "value", "unit"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every release should parse into tens of thousands of long records.
    An empty or tiny payload means the directory listing or the fixed-width
    table layout changed and parsing silently collapsed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 10000, f"{sid}: only {len(table)} rows (<10000)"
        assert EXPECTED_COLS.issubset(set(table.column_names)), (
            f"{sid}: columns {table.column_names} missing some of {EXPECTED_COLS}"
        )


def test_year_span_plausible(spec_ids):
    """GFED series start in 1997; the latest year must be recent. A truncated
    span signals a parse that dropped the wide year columns."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = table.column("year").to_pylist()
        assert min(years) == 1997, f"{sid}: min year {min(years)} != 1997"
        assert max(years) >= 2022, f"{sid}: max year {max(years)} < 2022"


def test_values_nonnegative(spec_ids):
    """Emissions are physical quantities and never negative."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = [v for v in table.column("value").to_pylist() if v is not None]
        assert vals, f"{sid}: every value is null"
        assert min(vals) >= 0, f"{sid}: negative emission value {min(vals)}"
