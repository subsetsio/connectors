"""Health invariants for the NHS Digital connector raw assets."""
from subsets_utils import load_raw_parquet

_EXPECTED_COLS = {"source_file", "row_index", "column", "value"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every package's melted raw asset must hold rows. An empty payload means
    the package's files.digital.nhs.uk resources disappeared or failed to parse."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_raw_schema_is_long_form(spec_ids):
    """Every raw asset must carry the uniform long schema; a drift here means
    the melt logic silently changed shape."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert set(table.column_names) == _EXPECTED_COLS, (
            f"{sid}: unexpected columns {table.column_names}"
        )


def test_values_present(spec_ids):
    """The `value` column should never be entirely null — that would mean every
    cell was dropped as empty, i.e. a parsing failure."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("value")
        assert col.null_count < len(table), f"{sid}: all values are null"
