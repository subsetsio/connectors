"""Health-invariant tests for the Ivey PMI connector raw assets.

Run post-DAG, in-connector, through subsets_utils loaders — catches silent
degradation (empty payload, a dropped table, a header/format change) that mere
file existence would miss.
"""

from subsets_utils import load_raw_parquet


def test_raw_nonempty_and_both_variants(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"
        variants = set(table.column("seasonal_adjustment").to_pylist())
        assert variants == {"seasonally_adjusted", "not_seasonally_adjusted"}, (
            f"{sid}: expected both seasonal-adjustment variants, got {variants} "
            "(a table likely failed to parse)"
        )


def test_index_values_in_diffusion_range(spec_ids):
    """Diffusion indices are bounded 0-100; out-of-range means a parse/column
    misalignment slipped a wrong value into a numeric column."""
    cols = [
        "ivey_pmi",
        "employment_index",
        "inventories_index",
        "deliveries_index",
        "prices_index",
    ]
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        for col in cols:
            vals = [v for v in table.column(col).to_pylist() if v is not None]
            assert vals, f"{sid}: column {col} is entirely null"
            assert min(vals) >= 0 and max(vals) <= 100, (
                f"{sid}: {col} out of 0-100 range (min={min(vals)}, max={max(vals)})"
            )
