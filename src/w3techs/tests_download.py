"""Post-DAG health invariants for the W3Techs raw asset. These run in-connector
through subsets_utils loaders, so they behave identically locally and on CI."""
from subsets_utils import load_raw_parquet

EXPECTED_CATEGORIES = 27


def test_raw_nonempty(spec_ids):
    """Empty payload usually means the page layout changed or every fetch was
    silently dropped."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_all_categories_present(spec_ids):
    """Every one of the 27 survey categories must contribute rows; fewer means a
    category's trend pages both 404'd or the table picker missed them."""
    table = load_raw_parquet("w3techs-values")
    cats = set(table.column("category").to_pylist())
    assert len(cats) == EXPECTED_CATEGORIES, (
        f"expected {EXPECTED_CATEGORIES} categories, got {len(cats)}: {sorted(cats)}"
    )


def test_metric_values(spec_ids):
    """Metric is the discriminator between the two trend views; an unexpected
    value means a parsing/labelling bug."""
    table = load_raw_parquet("w3techs-values")
    metrics = set(table.column("metric").to_pylist())
    assert metrics <= {"market_share", "usage"}, f"unexpected metric values: {metrics}"
    assert metrics, "no metric values present"


def test_percent_in_range(spec_ids):
    """Percentages are in (0, 100]; values outside mean a parse bug (e.g. failing
    to strip '%' or mis-aligning columns)."""
    table = load_raw_parquet("w3techs-values")
    vals = table.column("percent").to_pylist()
    bad = [v for v in vals if v is None or v < 0 or v > 100]
    assert not bad, f"{len(bad)} percent values out of [0,100] range; sample {bad[:5]}"
