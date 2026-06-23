"""Health-invariant tests for the IMDb connector — run post-DAG, in-connector.

These catch silent degradation that file-existence alone misses: a truncated
download, a switched format, an empty payload, or a header that drifted so the
expected key columns vanished.
"""

from subsets_utils import load_raw_parquet

# Each raw asset's expected key column(s) — the join keys that must survive any
# format change. If these disappear, parsing silently broke.
KEY_COLUMNS = {
    "imdb-title.basics": ["tconst", "titleType"],
    "imdb-title.ratings": ["tconst", "averageRating", "numVotes"],
    "imdb-title.akas": ["titleId", "ordering", "title"],
    "imdb-title.crew": ["tconst", "directors", "writers"],
    "imdb-title.episode": ["tconst", "parentTconst"],
    "imdb-title.principals": ["tconst", "nconst", "category"],
    "imdb-name.basics": ["nconst", "primaryName"],
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download produced a parquet with rows. Empty = truncated/format flip."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_key_columns_present(spec_ids):
    """Key columns must be present — a header drift would drop them silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        cols = set(table.column_names)
        expected = KEY_COLUMNS.get(sid, [])
        missing = [c for c in expected if c not in cols]
        assert not missing, f"{sid}: missing expected columns {missing} (have {sorted(cols)})"


def test_id_columns_well_formed(spec_ids):
    """Sample the leading id column and confirm the IMDb id format held — a
    parsing offset (wrong delimiter) would scramble these immediately."""
    prefix = {
        "imdb-title.basics": "tt", "imdb-title.ratings": "tt",
        "imdb-title.akas": "tt", "imdb-title.crew": "tt",
        "imdb-title.episode": "tt", "imdb-title.principals": "tt",
        "imdb-name.basics": "nm",
    }
    first_col = {
        "imdb-title.akas": "titleId",
    }
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = first_col.get(sid, table.column_names[0])
        sample = table.column(col).slice(0, 1000).to_pylist()
        bad = [v for v in sample if v is not None and not v.startswith(prefix[sid])]
        assert not bad, f"{sid}: {len(bad)}/1000 ids in {col!r} not '{prefix[sid]}…': {bad[:3]}"
