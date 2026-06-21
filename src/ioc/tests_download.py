"""Health invariants for the IOC medal-table raw asset."""
from subsets_utils import load_raw_parquet


def test_medal_table_nonempty(spec_ids):
    """Every download spec's raw parquet should hold rows. An empty payload
    means both the live origin and the Wayback fallback returned nothing
    (format change, archive gone, or enumeration broke)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_both_editions_present(spec_ids):
    """The feed should carry both 2024 Games editions. If one is missing the
    per-edition fetch/fallback silently dropped it."""
    table = load_raw_parquet("ioc-medal-table")
    editions = set(table.column("edition").to_pylist())
    assert {"OG2024", "PG2024"} <= editions, f"missing editions: got {sorted(editions)}"


def test_overall_aggregate_and_medals(spec_ids):
    """sport='GLO' is the all-sports aggregate and must exist; total medal
    counts must be positive (guards against an all-null/zeroed payload)."""
    table = load_raw_parquet("ioc-medal-table")
    sports = set(table.column("sport").to_pylist())
    assert "GLO" in sports, f"all-sports aggregate sport='GLO' absent; sports={sorted(sports)[:10]}"
    totals = [t for t in table.column("total").to_pylist() if t is not None]
    assert totals and max(totals) > 0, "no positive medal totals in payload"
