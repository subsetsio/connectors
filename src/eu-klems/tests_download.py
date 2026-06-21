"""Post-DAG health invariants for the EU KLEMS connector.

Each raw asset is the long-normalized form of one bulk module: it must carry
rows, the core long columns (var/year/value), a plausible year span, and at
least some non-null values. Silent degradation (endpoint switched format,
truncated download, a layout we failed to melt) trips these.
"""
from subsets_utils import load_raw_parquet


def test_all_modules_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 1000, f"{sid}: only {len(table)} rows — truncated or wrong layout"


def test_core_long_columns(spec_ids):
    """Every module must normalize to the long shape with var/year/value."""
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).schema.names)
        missing = {"var", "year", "value", "country"} - cols
        assert not missing, f"{sid}: missing core long columns {missing}"


def test_year_span_plausible(spec_ids):
    """Years must fall in the documented 1995..2017 window of this release."""
    for sid in spec_ids:
        years = load_raw_parquet(sid).column("year").to_pylist()
        ymin, ymax = min(years), max(years)
        assert 1990 <= ymin <= 1996, f"{sid}: min year {ymin} outside expected range"
        assert 2015 <= ymax <= 2025, f"{sid}: max year {ymax} outside expected range"


def test_values_present(spec_ids):
    """At least some non-null values per module (all-null means the melt or
    numeric coercion silently nuked the data)."""
    for sid in spec_ids:
        vals = load_raw_parquet(sid).column("value")
        nonnull = len(vals) - vals.null_count
        assert nonnull > 0, f"{sid}: every value is null"
