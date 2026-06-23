"""Health invariants over the raw assets — catch silent degradation that file
existence alone misses (empty payloads, truncated streams, lost columns)."""

from subsets_utils import load_raw_parquet


def test_all_raw_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_year_column_present(spec_ids):
    """Every Atlas table is a yearly series; a missing 'year' means the CSV
    schema shifted or the wrong file was pulled."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert "year" in table.schema.names, f"{sid}: no 'year' column ({table.schema.names})"
