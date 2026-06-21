"""Health-invariant tests for the ECDC download stage."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every entity's CSV export should yield rows. An empty payload means the
    Atlas export endpoint changed shape or the (topic, dataset) pair stopped
    publishing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns(spec_ids):
    """The export schema must stay stable -- a column rename upstream would
    silently break the transforms."""
    expected = {
        "health_topic", "population", "indicator", "unit", "geo_level",
        "time_unit", "time", "region_code", "region_name", "num_value",
        "txt_value",
    }
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert cols == expected, f"{sid}: columns {cols} != {expected}"


def test_some_real_values(spec_ids):
    """Across all entities there must be a healthy number of non-null numeric
    measurements -- if every num_value is null, parsing of NumValue broke."""
    total_non_null = 0
    for sid in spec_ids:
        col = load_raw_parquet(sid).column("num_value")
        total_non_null += len(col) - col.null_count
    assert total_non_null > 1000, (
        f"only {total_non_null} non-null num_value across all assets; "
        f"NumValue parsing likely broke"
    )
