"""Health invariants for the FIDE rating-list raw asset.

These run post-DAG against the data as saved, catching silent degradation that
file-existence checks miss: a truncated download, an empty payload, or a parse
that produced rows with no actual ratings.
"""

from subsets_utils import load_raw_parquet


def test_players_nonempty(spec_ids):
    """The combined FIDE list holds ~1M+ players. A near-empty table means the
    download truncated or the XML format changed under us."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) >= 500_000, f"{sid}: only {len(table)} rows; expected >=500k"


def test_ratings_present(spec_ids):
    """A large share of players should carry a non-null, non-zero standard,
    rapid, or blitz rating. If every rating column is null/zero the parse mapped
    the wrong elements."""
    for sid in spec_ids:
        table = load_raw_parquet(sid).to_pydict()
        rated = sum(
            1
            for s, r, b in zip(table["rating"], table["rapid_rating"], table["blitz_rating"])
            if (s or 0) > 0 or (r or 0) > 0 or (b or 0) > 0
        )
        assert rated >= 100_000, f"{sid}: only {rated} players have any rating; parse likely broken"
