"""Health invariants for the Dallas Fed connector, run post-DAG in-connector."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must produce a non-empty parquet. An empty payload
    usually means the workbook URL moved or the sheet layout changed and our
    parser silently matched nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_no_null_dates(spec_ids):
    """Every row must carry a parsed date — null dates mean a date column or
    quarter label failed to parse and would be dropped downstream."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        if "date" not in table.column_names:
            continue
        nulls = table.column("date").null_count
        assert nulls == 0, f"{sid}: {nulls} rows with null date"


def test_value_columns_have_signal(spec_ids):
    """The numeric value column must have at least some non-null values — an
    all-null value column means every cell failed numeric coercion."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = "wei" if "wei" in table.column_names else "value"
        if col not in table.column_names:
            continue
        non_null = table.num_rows - table.column(col).null_count
        assert non_null > 0, f"{sid}: value column '{col}' is entirely null"
