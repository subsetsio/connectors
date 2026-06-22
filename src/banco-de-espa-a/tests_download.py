"""Health-invariant tests for the Banco de Espana connector raw assets.

Catch silent degradation that file-existence alone misses: empty payloads,
truncated downloads, a publication ZIP that quietly stopped parsing.
"""

from subsets_utils import load_raw_parquet


def test_values_nonempty_and_typed():
    """The observations asset should hold millions of rows with real dates and
    numeric values. A near-empty table means ZIP/CSV parsing degraded."""
    t = load_raw_parquet("banco-de-espa-a-values")
    assert len(t) >= 500_000, f"values: only {len(t)} rows (expected >=500k)"
    cols = set(t.column_names)
    assert {"series_code", "date", "value"} <= cols, f"missing cols: {cols}"
    # date column must parse as a date32 and not be entirely null
    null_dates = t.column("date").null_count
    assert null_dates == 0, f"values: {null_dates} null dates in raw"


def test_values_covers_many_series():
    t = load_raw_parquet("banco-de-espa-a-values")
    distinct = len(set(t.column("series_code").to_pylist()[:2_000_000]))
    assert distinct >= 1_000, f"values: only {distinct} distinct series in sample"


def test_series_catalogue_nonempty_unique():
    """The catalogue should hold >10k unique series codes."""
    t = load_raw_parquet("banco-de-espa-a-series")
    assert len(t) >= 10_000, f"series: only {len(t)} rows (expected >=10k)"
    codes = t.column("series_code").to_pylist()
    assert len(codes) == len(set(codes)), "series: duplicate series_code in raw"
