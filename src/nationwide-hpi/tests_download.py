"""Health invariants for the Nationwide HPI raw assets.

Each download node writes one uniform long-format parquet table
(date | period_label | category | measure | value). These tests catch silent
degradation: a spreadsheet whose layout changed (empty parse), a truncated
download, or values that stopped being numeric.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet must hold rows. An empty parse usually means the
    upstream spreadsheet layout changed and our family parser fell through."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_schema_and_values(spec_ids):
    """Columns present, value column populated, dates within a plausible range."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        assert {"date", "category", "measure", "value"} <= cols, f"{sid}: missing columns {cols}"
        values = table.column("value").to_pylist()
        assert any(v is not None for v in values), f"{sid}: all values null"
        years = {d.year for d in table.column("date").to_pylist() if d is not None}
        assert years, f"{sid}: no parseable dates"
        assert min(years) >= 1950 and max(years) <= 2035, f"{sid}: dates out of range {min(years)}..{max(years)}"


def test_corpus_breadth(spec_ids):
    """All 22 series should be present and the corpus should be substantial; a
    big drop means several spreadsheets failed to download or parse."""
    assert len(spec_ids) == 22, f"expected 22 download specs, got {len(spec_ids)}"
    total = sum(len(load_raw_parquet(sid)) for sid in spec_ids)
    assert total >= 40000, f"corpus only {total} rows across all series; expected >=40000"
