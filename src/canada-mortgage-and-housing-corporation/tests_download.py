"""Health-invariant tests run post-DAG, in-connector, through subsets_utils."""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every CMHC/StatCan table should hold rows. An empty payload means the
    resource URL changed, the zip layout changed, or parsing silently broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_core_columns_present(spec_ids):
    """The normalised StatCan long-format schema is fixed across every table."""
    required = {"product_id", "ref_date", "geo", "vector", "value"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = required - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_ref_date_populated(spec_ids):
    """Every observation row carries a reference period."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        nulls = table.column("ref_date").null_count
        assert nulls == 0, f"{sid}: {nulls}/{len(table)} rows have null ref_date"
