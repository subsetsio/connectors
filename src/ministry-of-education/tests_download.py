"""Health invariants for the MoE (China) download assets.

These run post-DAG, in-connector, against the raw assets via subsets_utils
loaders — catching silent degradation (empty payloads, parser that stopped
matching articles, a year-index format change) that file existence alone misses.
"""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every table type is published in at least the most recent year, so each
    raw asset must hold rows. An empty asset means the parser stopped matching
    the article title (site layout/title drift) or the index format changed."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_values_are_finite_numbers(spec_ids):
    """The body cells we keep are numeric; a column that came back all-null
    means the numeric/header detection misfired for this table's layout."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("value")
        assert col.null_count < len(col), f"{sid}: every parsed value is null"


def test_years_plausible(spec_ids):
    """Statistical years live in the published 1997..2026 window; anything
    outside means a stray cell got parsed as a year somewhere upstream."""
    for sid in spec_ids:
        years = load_raw_parquet(sid).column("year").to_pylist()
        bad = [y for y in years if y is None or y < 1997 or y > 2026]
        assert not bad, f"{sid}: implausible years {sorted(set(bad))[:5]}"
