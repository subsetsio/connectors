from subsets_utils import load_raw_parquet


def test_series_catalog_populated():
    """The /Series catalog should hold ~117 series; a big drop means the
    catalog endpoint changed shape or returned an error envelope."""
    t = load_raw_parquet("sveriges-riksbank-series")
    assert len(t) >= 80, f"series catalog has {len(t)} rows; expected ~117 (>=80)"
    cols = set(t.column_names)
    assert {"series_id", "group_id", "observation_min_date"} <= cols, f"missing cols: {cols}"


def test_values_populated():
    """Long-format observations should hold many rows across many series."""
    t = load_raw_parquet("sveriges-riksbank-values")
    assert len(t) > 10000, f"values has only {len(t)} rows; expected tens of thousands"
    import pyarrow.compute as pc
    distinct_series = pc.count_distinct(t.column("series_id")).as_py()
    assert distinct_series >= 80, f"only {distinct_series} distinct series in values; expected ~117"


def test_values_numeric():
    """Values must parse as real numbers, not nulls/strings."""
    t = load_raw_parquet("sveriges-riksbank-values")
    import pyarrow.compute as pc
    non_null = pc.sum(pc.is_valid(t.column("value"))).as_py()
    assert non_null > 0, "every observation value is null — parsing broke"
