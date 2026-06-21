"""Health-invariant tests for the Global Carbon Project connector.

Run post-DAG, in-connector. They read raw through the same loader the download
node used (parquet) and assert properties that catch silent degradation a
file-exists check would miss: empty payloads, a workbook whose layout shifted so
parsing silently dropped to a handful of rows, or a column that went all-null.
"""
from subsets_utils import load_raw_parquet

SLUG = "global-carbon-project"


def test_all_raw_assets_nonempty(spec_ids):
    """Every subset's raw parquet must hold rows. Zero rows means the workbook
    download or the sheet parse silently failed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_value_column_not_all_null(spec_ids):
    """Each subset carries a numeric `value` column with real (non-null) data."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert "value" in table.column_names, f"{sid}: missing 'value' column"
        col = table.column("value")
        assert col.null_count < len(table), f"{sid}: 'value' is entirely null"


def test_national_territorial_breadth(spec_ids):
    """The flagship national territorial table must keep broad country and year
    coverage — a collapsed header would shrink one of these sharply."""
    sid = f"{SLUG}-national-fossil-territorial-emissions"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    df = table.to_pydict()
    assert len(set(df["country"])) >= 150, "territorial: <150 distinct countries"
    years = set(df["year"])
    assert min(years) <= 1900, "territorial: history does not reach back to 1900"
    assert max(years) >= 2020, "territorial: missing recent years (>=2020)"


def test_global_budget_has_components(spec_ids):
    """The headline global budget must expose its multi-component breakdown."""
    sid = f"{SLUG}-global-carbon-budget"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    series = set(table.to_pydict()["series"])
    assert len(series) >= 5, f"global-carbon-budget: only {len(series)} series"
