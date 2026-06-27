"""Health invariants for the nationwide raw assets (long-format parquet:
date, period, series, value). Catches silent degradation a file-exists check
misses — empty payloads, a parser that collapsed all columns to one series,
or values that all came back null."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns(spec_ids):
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert {"date", "period", "series", "value"} <= cols, \
            f"{sid}: missing expected columns, got {sorted(cols)}"


def test_value_not_all_null(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        val = table.column("value")
        assert val.null_count < len(val), f"{sid}: every value is null"


def test_series_not_collapsed(spec_ids):
    """Most files publish many series (regions/measures/occupations). If a
    multi-series file suddenly has 1 series, the header parse regressed
    (e.g. the col1..colN fallback). Single-series files are exempt."""
    single = {"nationwide-chart-data-download-annual-percentage-change-in-uk-house-prices",
              "nationwide-not-new-prop"}
    for sid in spec_ids:
        if sid in single:
            continue
        n = len(set(load_raw_parquet(sid).column("series").to_pylist()))
        assert n >= 2, f"{sid}: only {n} distinct series — header parse likely broke"
