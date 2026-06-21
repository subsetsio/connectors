"""Health-invariant tests for the WIPO connector raw assets.

Run post-DAG, in-connector, against the raw parquet each download node wrote.
They catch silent degradation that mere file-existence misses: empty payloads,
a backend that started returning null envelopes, year/value columns going junk.
"""
from subsets_utils import load_raw_parquet

# Subsets that carry the office/origin long-format schema.
_OFFICE_COLS = {
    "office", "origin", "indicator_id", "indicator",
    "report_type", "year", "breakdown_index", "value",
}
_KEY_COLS = {
    "indicator_id", "indicator", "ip_right", "office",
    "origin", "year", "breakdown_index", "value",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw parquet must hold rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns(spec_ids):
    """Each asset exposes the long-format columns its transform reads."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        expected = _KEY_COLS if sid == "wipo-key-indicators" else _OFFICE_COLS
        missing = expected - cols
        assert not missing, f"{sid}: missing columns {missing}"


def test_years_and_values_sane(spec_ids):
    """Years fall in a plausible range and values are real numbers."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        years = table.column("year").to_pylist()
        assert years, f"{sid}: no year values"
        assert min(years) >= 1960, f"{sid}: implausible min year {min(years)}"
        assert max(years) <= 2100, f"{sid}: implausible max year {max(years)}"
        # value column is non-null by construction (parser only emits parsed floats)
        values = table.column("value")
        assert values.null_count == 0, f"{sid}: {values.null_count} null values leaked"
