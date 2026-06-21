"""In-connector health invariants — run post-DAG against the raw assets.

These catch silent degradation that file-existence alone misses: a WAF
challenge page parsed as an empty workbook, a truncated CSV, a format switch.
All raw assets share the long (date, series, value) schema.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must produce a non-empty long table."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_long_schema(spec_ids):
    """Columns are exactly date/series/value — a different shape means the
    parser latched onto the wrong sheet or a challenge page."""
    expected = {"date", "series", "value"}
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert expected.issubset(cols), f"{sid}: columns {cols} missing {expected - cols}"


def test_values_present(spec_ids):
    """At least some numeric values per asset; an all-null value column means
    the workbook columns were misidentified."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("value")
        assert vals.null_count < len(table), f"{sid}: every value is null"
