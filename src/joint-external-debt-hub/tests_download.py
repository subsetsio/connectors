from subsets_utils import load_raw_parquet


def test_values_nonempty(spec_ids):
    """The single values asset must hold observations. An empty payload means
    the Advanced API envelope changed or auth/format broke silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_values_have_some_non_null(spec_ids):
    """At least some observations must carry an actual numeric value — the API
    returns many null cells, but an all-null pull signals a parse/shape break."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("value")
        non_null = len(table) - vals.null_count
        assert non_null > 0, f"{sid}: every value is null ({len(table)} rows)"


def test_multiple_series_present(spec_ids):
    """The long-format table should span many series — collapsing to one series
    would mean the series-discovery loop broke."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        n_series = pc.count_distinct(table.column("series_code")).as_py()
        assert n_series >= 10, f"{sid}: only {n_series} distinct series (expected ~28)"
