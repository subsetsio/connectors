from subsets_utils import load_raw_parquet

EXPECTED_COLUMNS = {
    "delivery_date",
    "slot",
    "system_price",
    "area_price_tokyo",
    "area_price_kansai",
    "contract_volume_kwh",
}


def test_spot_raw_nonempty(spec_ids):
    """The spot raw parquet should hold the full multi-year corpus. Empty or
    tiny payloads usually mean the CSV endpoint changed format/encoding or the
    year-walk broke after the first 404."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 100000, f"{sid}: raw parquet has only {len(table)} rows"


def test_spot_schema(spec_ids):
    """Core columns must be present — guards against a silent header shift in
    the Shift-JIS CSV (positional parsing would then read the wrong columns)."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = EXPECTED_COLUMNS - cols
        assert not missing, f"{sid}: missing expected columns {missing}"
