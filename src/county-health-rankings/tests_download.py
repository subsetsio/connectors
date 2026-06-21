"""Health-invariant tests for County Health Rankings raw assets.

Run post-DAG inside the connector; they read raw through subsets_utils loaders,
so they behave identically locally and in the cloud. They guard against silent
degradation (truncated downloads, format switches, an empty unpivot) that mere
file existence misses.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_trends_shape():
    t = load_raw_parquet("county-health-rankings-trends")
    assert len(t) > 100_000, f"trends only {len(t)} rows; expected the full cumulative panel"
    cols = set(t.column_names)
    for c in ("yearspan", "measure_id", "fips", "raw_value"):
        assert c in cols, f"trends missing column {c}"
    # The trends file should span many measures and many years.
    assert t.column("measure_name").to_pylist().count(None) < len(t), "trends measure_name all null"


def test_analytic_shape():
    a = load_raw_parquet("county-health-rankings-analytic")
    assert len(a) > 1_000_000, f"analytic only {len(a)} rows; a year may have failed to parse"
    cols = set(a.column_names)
    for c in ("release_year", "measure_id", "fips", "raw_value"):
        assert c in cols, f"analytic missing column {c}"
    years = set(y for y in a.column("release_year").to_pylist() if y is not None)
    assert len(years) >= 8, f"analytic spans only {len(years)} release years; expected the full 2010-present set"
