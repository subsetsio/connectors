"""Health invariants for the Afrobarometer raw assets, run post-DAG in-connector."""

from subsets_utils import load_raw_parquet


def test_questions_catalog_nonempty():
    """The variable catalog should hold thousands of rows; a near-empty table
    means a round index call silently returned nothing."""
    t = load_raw_parquet("afrobarometer-questions")
    assert len(t) >= 3000, "questions catalog has only %d rows" % len(t)
    assert "variable_code" in t.column_names


def test_values_nonempty_and_shaped():
    """Aggregated statistics must be substantial and carry the key dimensions."""
    t = load_raw_parquet("afrobarometer-values")
    assert len(t) >= 200000, "values has only %d rows" % len(t)
    for col in ("variable_code", "country", "round_num", "pct_valid"):
        assert col in t.column_names, "values missing column %s" % col


def test_values_country_coverage():
    """Many distinct countries should be present — a collapse to a handful
    means the country-cross or sample union broke."""
    t = load_raw_parquet("afrobarometer-values")
    countries = set(t.column("country").to_pylist())
    assert len(countries) >= 30, "only %d distinct countries in values" % len(countries)
