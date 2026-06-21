"""Health-invariant tests run post-DAG, in-connector, through subsets_utils."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every GGDC dataset must produce a non-empty tidy table. An empty payload
    means the file moved/renamed in Dataverse or the workbook layout changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_value_column_present(spec_ids):
    """Every parser yields a numeric `value` column; its absence means a parser
    fell through or the sheet schema drifted."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert "value" in table.column_names, f"{sid}: no `value` column"


def test_no_null_values(spec_ids):
    """Parsers drop null observations before saving — a null in `value` means a
    coercion path regressed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        nulls = table.column("value").null_count
        assert nulls == 0, f"{sid}: {nulls} null values survived"
