"""Health invariants for V-Dem raw downloads.

Each raw asset is the wide all-varchar mirror of a V-Dem product CSV: hundreds
of indicator columns and one row per country-year (or country-date). These
tests catch silent degradation the file-exists check misses — a truncated
download, a format switch, or the identifier/indicator columns vanishing.
"""

from subsets_utils import load_raw_parquet


def test_raw_assets_wide_and_nonempty(spec_ids):
    """Every product mirror must hold many rows and stay very wide (the V-Dem
    products carry ~1900-4600 columns). A narrow or empty table means the ZIP
    member changed or the download truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 5000, f"{sid}: only {table.num_rows} rows"
        assert table.num_columns > 1000, f"{sid}: only {table.num_columns} columns"


def test_identifier_columns_present(spec_ids):
    """The five identifier columns the transform groups on must exist in every
    product, else the reshape silently drops its keys."""
    expected = {"country_name", "country_text_id", "country_id", "year", "historical_date"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = expected - cols
        assert not missing, f"{sid}: missing identifier columns {missing}"


def test_flagship_index_present(spec_ids):
    """v2x_polyarchy (the Electoral Democracy Index) is V-Dem's flagship measure
    and present in every product; its absence means the schema changed."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert "v2x_polyarchy" in cols, f"{sid}: flagship v2x_polyarchy column absent"
