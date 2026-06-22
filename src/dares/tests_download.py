"""Health-invariant tests for the DARES connector, run post-DAG in-connector."""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset's parquet export should hold rows. An empty payload means
    the ODS export endpoint changed format/path or silently returned nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_all_raw_assets_have_columns(spec_ids):
    """Each export must carry at least two columns — these are statistical
    tables (>=1 dimension + >=1 value); a single-column result is degraded."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_columns >= 2, (
            f"{sid}: only {table.num_columns} column(s); expected a real table"
        )
