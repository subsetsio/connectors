"""Health-invariant tests for the Christmas Bird Count connector.

Run post-DAG, in-connector, against the raw assets through subsets_utils
loaders. These catch silent degradation that file-existence alone misses:
empty/truncated crawls and structural drift in the multi-section CSV parse.
"""
from subsets_utils import load_raw_parquet


def test_observations_nonempty_and_shaped():
    t = load_raw_parquet("christmas-bird-count-observations")
    assert len(t) > 200_000, f"observations has only {len(t)} rows — crawl likely truncated"
    cols = set(t.column_names)
    expected = {
        "circle_id", "common_name", "scientific_name", "count_year",
        "season_year", "count_date", "how_many", "count_week_only",
        "number_per_party_hours", "flags",
    }
    assert expected <= cols, f"observations missing columns: {expected - cols}"


def test_observations_many_circles():
    """The whole point of the crawl is hemisphere-wide coverage; a handful of
    circles means the cid-band scan broke after the first hits."""
    t = load_raw_parquet("christmas-bird-count-observations")
    n_circles = len(set(t.column("circle_id").to_pylist()))
    assert n_circles > 500, f"observations span only {n_circles} circles — expected thousands"


def test_circles_nonempty_and_unique():
    t = load_raw_parquet("christmas-bird-count-circles")
    assert len(t) > 1000, f"circles has only {len(t)} rows — band scan likely truncated"
    ids = t.column("circle_id").to_pylist()
    assert len(ids) == len(set(ids)), "duplicate circle_id in circles reference table"
