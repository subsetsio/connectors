"""Post-run health invariants for the GACC monthly-bulletin scrape.

These run in-connector after the DAG, loading raw via the same loader the
download node used (save_raw_parquet -> load_raw_parquet).
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every table's melted raw asset must hold rows. Empty means the listing
    or page layout changed and parsing silently produced nothing."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_and_values_sane(spec_ids):
    """Schema must match the melt contract and values must be real numbers
    (not all-null), guarding against a column-shift in the HTML grid."""
    expected = {"year", "month", "period_label", "col_header", "value", "source_url"}
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert expected <= cols, f"{sid}: missing columns {expected - cols}"
        values = table.column("value").to_pylist()
        non_null = [v for v in values if v is not None]
        assert non_null, f"{sid}: every 'value' is null"
        labels = [x for x in table.column("period_label").to_pylist() if x]
        assert labels, f"{sid}: no non-empty period_label"


def test_country_table_has_expected_breadth(spec_ids):
    """The country table (table 02) should carry many distinct period labels
    (countries/regions). If pagination/parse broke we'd see a handful."""
    sid = "china-customs-gacc-table-02-imports-and-exports-by-country-region-of-origin-destination"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    distinct_labels = set(table.column("period_label").to_pylist())
    assert len(distinct_labels) >= 50, (
        f"{sid}: only {len(distinct_labels)} distinct period labels; "
        f"expected >=50 countries/regions"
    )
