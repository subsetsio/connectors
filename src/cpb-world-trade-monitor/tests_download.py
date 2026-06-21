"""Health invariants for the CPB World Trade Monitor raw assets."""
from subsets_utils import load_raw_parquet


def test_series_catalog_shape(spec_ids):
    """The series catalog should hold ~88 series (60 trade + 28 industrial
    production). A big drop means the workbook layout or parsing changed."""
    t = load_raw_parquet("cpb-world-trade-monitor-series")
    assert len(t) >= 80, f"series catalog has only {len(t)} rows; expected >=80"
    cols = set(t.column_names)
    assert {"series_code", "variable", "region", "measure"} <= cols, cols
    sheets = set(t.column("sheet").to_pylist())
    assert sheets == {"trade_out", "inpro_out"}, f"sheets present: {sheets}"


def test_values_long_format(spec_ids):
    """Long-format observations: ~88 series x ~315 months. Should be tens of
    thousands of non-null rows, and every series_code must exist in the catalog."""
    v = load_raw_parquet("cpb-world-trade-monitor-values")
    assert len(v) >= 20000, f"values has only {len(v)} rows; expected >=20000"
    assert {"series_code", "period", "value"} <= set(v.column_names)
    # No null values should be stored (we only emit numeric cells).
    assert v.column("value").null_count == 0, "unexpected null values in raw"

    s = load_raw_parquet("cpb-world-trade-monitor-series")
    catalog_codes = set(s.column("series_code").to_pylist())
    value_codes = set(v.column("series_code").to_pylist())
    orphans = value_codes - catalog_codes
    assert not orphans, f"value series_codes missing from catalog: {sorted(orphans)[:5]}"


def test_history_depth(spec_ids):
    """Each release is a full snapshot back to 2000m01; expect coverage from
    2000 to recent. Checks the earliest and that we span 20+ years."""
    v = load_raw_parquet("cpb-world-trade-monitor-values")
    periods = sorted(set(v.column("period").to_pylist()))
    assert periods[0] == "2000-01-01", f"earliest period is {periods[0]}"
    assert periods[-1] >= "2024-01-01", f"latest period is {periods[-1]} (stale?)"
