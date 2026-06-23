"""Health invariants for the JODI-Oil raw download. Catches silent degradation
that file existence alone misses — a tier that 404'd, a truncated zip, a format
switch."""

from subsets_utils import load_raw_parquet

EXPECTED_COLS = {
    "ref_area", "time_period", "energy_product", "flow_breakdown",
    "unit_measure", "obs_value", "assessment_code", "tier",
}


def test_values_nonempty_and_shaped(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"
        cols = set(table.column_names)
        missing = EXPECTED_COLS - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_both_tiers_present(spec_ids):
    """Both corpus zips must have parsed — losing one silently halves coverage."""
    for sid in spec_ids:
        tiers = set(load_raw_parquet(sid).column("tier").to_pylist())
        assert {"primary", "secondary"} <= tiers, f"{sid}: tiers present = {tiers}"
