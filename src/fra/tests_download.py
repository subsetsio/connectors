from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every FRA dataset has tens of thousands to millions of rows; an empty or
    near-empty parquet means the Socrata export truncated or the CSV stream
    aborted before any rows were written."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 1000, f"{sid}: raw parquet has only {len(table)} rows"


def test_all_columns_present(spec_ids):
    """The all-string export schema must carry real columns (the CSV header);
    a single-column or zero-column table means header parsing broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_columns >= 5, (
            f"{sid}: only {table.num_columns} columns; header parse likely failed"
        )
