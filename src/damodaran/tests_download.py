"""Health invariants for the Damodaran raw assets — catch silent degradation
(empty payloads, format change, a parser that stopped finding the table)."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every family's long table should hold rows. Empty means the .xls layout
    moved and the anchor-based parser found no table."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_long_schema_present(spec_ids):
    """Raw is the uniform long schema [region, category, metric, value]."""
    expected = {"region", "category", "metric", "value"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        assert expected <= cols, f"{sid}: columns {cols} missing {expected - cols}"


def test_values_are_finite_numbers(spec_ids):
    """The melted value column must be real numbers — a parse that swept in
    header/label text would surface as nulls here."""
    import math
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        vals = table.column("value").to_pylist()
        bad = [v for v in vals if v is None or not math.isfinite(v)]
        assert not bad, f"{sid}: {len(bad)} non-finite/null values in 'value'"
