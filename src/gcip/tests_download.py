"""Health-invariant tests for the GCIP download node.

These run post-DAG, in-connector, reading raw through subsets_utils loaders so
they behave identically locally and in the cloud. They catch silent
degradation that file existence alone misses (empty payload, truncated parse,
unit/scale shift).
"""

from subsets_utils import load_raw_parquet


def test_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. An empty payload usually
    means the GitHub raw URL changed shape or returned an error body."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_full_panel_rows(spec_ids):
    """The GCIP income panel is ~4900 country-year rows (~144 countries x
    1980-2015). A drastically smaller count means the parse truncated (e.g.
    preamble handling broke or the file was paginated)."""
    table = load_raw_parquet("gcip-gcip-income-deciles")
    assert len(table) >= 4000, f"gcip-income-deciles: only {len(table)} rows; expected ~4900"


def test_decile_ordering(spec_ids):
    """Within every row, income deciles must be monotonically non-decreasing
    (D1 <= D2 <= ... <= D10). A violation means columns got shuffled."""
    table = load_raw_parquet("gcip-gcip-income-deciles")
    cols = [table.column(f"decile_{i}_income").to_pylist() for i in range(1, 11)]
    for r in range(table.num_rows):
        vals = [cols[i][r] for i in range(10)]
        assert vals == sorted(vals), f"row {r}: deciles not ordered: {vals}"
