"""Health-invariant tests — run post-DAG, in-connector, against the raw assets
the download nodes wrote. Catch silent degradation that file-existence misses:
empty payloads, a vanished votes column, a tarball that 404'd into nothing.
"""
from subsets_utils import load_raw_parquet


def test_all_states_nonempty(spec_ids):
    """Every accepted state repo has thousands of result rows; an empty parquet
    means the tarball fetch or the CSV parse silently broke for that state."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_core_columns_present(spec_ids):
    """The normalised core schema must survive; a missing column means the
    fetch fn schema drifted away from the transform's expectations."""
    required = {"state", "election_date", "reporting_level", "office",
                "candidate", "votes"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        missing = required - cols
        assert not missing, f"{sid}: missing core columns {sorted(missing)}"


def test_votes_mostly_populated(spec_ids):
    """votes is the payload — if it is entirely null for a state, the vote
    column was misdetected or the source changed format."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        col = table.column("votes")
        nonnull = len(col) - col.null_count
        assert nonnull > 0, f"{sid}: votes column is entirely null"
