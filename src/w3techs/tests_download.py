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
    """The long-format table must cover all 27 survey categories; fewer means a
    category page 404'd or the table picker missed it for some slug."""
    table = load_raw_parquet("w3techs-values")
    cats = set(table.column("category").to_pylist())
    assert len(cats) == EXPECTED_CATEGORIES, (
        f"expected {EXPECTED_CATEGORIES} categories, got {len(cats)}: {sorted(cats)}"
    )


def test_percent_in_range(spec_ids):
    """Market share is a percentage in (0, 100]; values outside mean a parse
    bug (e.g. failing to strip '%' or mis-aligning columns)."""
    table = load_raw_parquet("w3techs-values")
    vals = table.column("market_share_percent").to_pylist()
    bad = [v for v in vals if v is None or v < 0 or v > 100]
    assert not bad, f"{len(bad)} market-share values out of [0,100] range; sample {bad[:5]}"
