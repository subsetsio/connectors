"""Health-invariant tests for the Nareit connector raw assets."""
from subsets_utils import load_raw_parquet


def test_monthly_returns_nonempty():
    """The monthly returns asset must hold rows. Empty means the .xls layout
    changed or every download silently failed."""
    table = load_raw_parquet("nareit-monthly-returns")
    assert len(table) > 1000, f"nareit-monthly-returns: only {len(table)} rows"


def test_all_index_groups_present():
    """All three index groups must appear; a missing group means a whole class
    of files (headline or a sector layout) failed to parse."""
    table = load_raw_parquet("nareit-monthly-returns")
    groups = set(table.column("group").to_pylist())
    assert {"headline", "equity-sector", "mortgage-sector"} <= groups, (
        f"missing index groups, got {groups}"
    )


def test_index_breadth():
    """We expect the 6 headline indexes plus ~21 property sectors. A sharp drop
    means several per-sector files stopped resolving."""
    table = load_raw_parquet("nareit-monthly-returns")
    n = len(set(table.column("index").to_pylist()))
    assert n >= 25, f"only {n} distinct indexes; expected >=25 (6 headline + ~21 sectors)"


def test_recent_coverage():
    """Headline history must reach a recent year; a stale max date means the
    historical file stopped updating or parsing truncated."""
    table = load_raw_parquet("nareit-monthly-returns")
    max_year = max(d.year for d in table.column("date").to_pylist())
    assert max_year >= 2024, f"latest date year is {max_year}; expected >=2024"
