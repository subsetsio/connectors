from subsets_utils import load_raw_parquet, load_raw_ndjson


def test_values_nonempty_and_shaped():
    """The values asset should hold many long-format observations with the
    expected columns and at least a few hundred distinct indicators."""
    table = load_raw_parquet("gapminder-values")
    assert len(table) > 100_000, f"values has too few rows: {len(table)}"
    cols = set(table.column_names)
    assert {"repo", "geo_dim", "geo", "time", "indicator", "value"} <= cols, cols
    indicators = set(table.column("indicator").to_pylist())
    assert len(indicators) > 300, f"too few distinct indicators: {len(indicators)}"
    repos = set(table.column("repo").to_pylist())
    assert {"systema_globalis", "fasttrack"} <= repos, repos


def test_concepts_nonempty():
    """The concepts catalog should carry many indicator records from both repos."""
    rows = load_raw_ndjson("gapminder-concepts")
    assert len(rows) > 500, f"too few concepts: {len(rows)}"
    assert any(r.get("name") for r in rows), "no concept has a name"
    repos = {r.get("repo") for r in rows}
    assert {"systema_globalis", "fasttrack"} <= repos, repos
