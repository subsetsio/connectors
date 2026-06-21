"""Post-DAG health invariants for the UIS connector raw assets."""
from subsets_utils import load_raw_parquet

SLUG = "unesco-institute-for-statistics"


def test_indicators_nonempty_and_themed():
    """The indicator catalog should hold thousands of rows across all four
    UIS themes; <1000 rows or a missing theme means the catalog endpoint
    returned a partial/changed payload."""
    t = load_raw_parquet(f"{SLUG}-indicators")
    assert t.num_rows >= 1000, f"indicators: {t.num_rows} rows; expected ~5000"
    themes = set(t.column("theme").to_pylist())
    expected = {
        "EDUCATION",
        "SCIENCE_TECHNOLOGY_INNOVATION",
        "CULTURE",
        "DEMOGRAPHIC_SOCIOECONOMIC",
    }
    missing = expected - themes
    assert not missing, f"indicators: missing themes {missing}"


def test_geounits_reasonable():
    """~462 geo units across NATIONAL + REGIONAL."""
    t = load_raw_parquet(f"{SLUG}-geounits")
    assert t.num_rows >= 200, f"geounits: {t.num_rows} rows; expected >=200"
    types = set(t.column("type").to_pylist())
    assert "NATIONAL" in types, f"geounits: no NATIONAL units (types={types})"


def test_values_corpus_substantial():
    """The full corpus is ~8.6M observations; a fraction of that means the
    per-indicator crawl broke partway. Also sanity-check the join keys and
    that more than a handful of distinct indicators are present."""
    t = load_raw_parquet(f"{SLUG}-values")
    assert t.num_rows >= 5_000_000, f"values: only {t.num_rows} rows; expected ~8.6M"
    n_ind = len(set(t.column("indicator_id").to_pylist()[:200000]))
    assert n_ind >= 100, f"values: only {n_ind} distinct indicators in head sample"
    # value column must carry real numbers, not be all-null
    vals = t.column("value").to_pylist()[:100000]
    assert any(v is not None for v in vals), "values: 'value' column is all-null in head"
