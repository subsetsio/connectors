from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    """The full Fatal Encounters corpus is ~31k rows; a tiny payload means the
    Google Sheet export changed format or returned an HTML error page."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 20000, f"{sid}: got {len(table)} rows, expected >=20000"


def test_expected_columns(spec_ids):
    """Header drift in the sheet would silently drop columns; assert the core
    fields survived the parse."""
    expected = {"unique_id", "name", "date_of_death", "state", "agency", "latitude"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = expected - cols
        assert not missing, f"{sid}: missing expected columns {missing}"
