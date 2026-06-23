"""Health-invariant tests for the PPR raw download.

Run post-DAG, in-connector, through subsets_utils loaders — they catch silent
degradation (truncated download, format switch, empty payload) that file
existence alone misses."""

from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "file_year",
    "date_of_sale",
    "address",
    "county",
    "eircode",
    "price",
    "not_full_market_price",
    "vat_exclusive",
    "description_of_property",
    "property_size_description",
}


def test_transactions_nonempty_and_large(spec_ids):
    """The register holds ~1M sales across 2010-present. <500k rows means the
    per-year crawl stopped early or the source truncated a file."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 500_000, f"{sid}: only {len(table)} rows; expected >=500k"


def test_transactions_schema(spec_ids):
    """Column set must be exactly the faithful 9-column CSV layout plus file_year.
    A drift here means the source changed its header."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert cols == EXPECTED_COLUMNS, f"{sid}: unexpected columns {cols ^ EXPECTED_COLUMNS}"


def test_multiple_years_present(spec_ids):
    """The corpus spans many calendar years; a single distinct file_year would
    mean the discovery loop stopped after year one."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = set(table.column("file_year").to_pylist())
        assert len(years) >= 10, f"{sid}: only {len(years)} distinct file_year values"
