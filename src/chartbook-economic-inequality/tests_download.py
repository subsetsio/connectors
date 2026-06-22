from subsets_utils import load_raw_parquet


def test_raw_nonempty(spec_ids):
    """The single raw asset should hold the full long table. An empty or tiny
    payload means the .xls download switched format or was truncated."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 15000, f"{sid}: raw parquet has only {len(table)} rows"


def test_has_real_values(spec_ids):
    """Most slots are blank, but a healthy pull has thousands of real values.
    Zero non-null values means parsing or the source columns broke."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("value")
        non_null = len(table) - col.null_count
        assert non_null > 3000, f"{sid}: only {non_null} non-null values"
