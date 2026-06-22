from subsets_utils import load_raw_parquet


def test_raw_nonempty_and_paneled(spec_ids):
    """The HFI raw asset must hold the full multi-decade panel. An empty or
    truncated payload usually means the static file URL moved (new edition) or
    the download was cut short."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows >= 3000, f"{sid}: only {table.num_rows} rows; expected the full ~3960-row panel"
        cols = set(table.column_names)
        for required in ("year", "iso", "countries", "hf_score"):
            assert required in cols, f"{sid}: missing expected column '{required}'"


def test_wide_indicator_schema(spec_ids):
    """HFI is a wide panel (~155 columns of personal/economic freedom
    indicators). A collapse to a handful of columns means the source changed
    format."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_columns >= 100, f"{sid}: only {table.num_columns} columns; expected a wide >=100-column panel"


def test_jurisdiction_coverage(spec_ids):
    """Should span ~165 jurisdictions; a steep drop signals partial coverage."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        n_iso = pc.count_distinct(table.column("iso")).as_py()
        assert n_iso >= 150, f"{sid}: only {n_iso} distinct jurisdictions; expected ~165"
