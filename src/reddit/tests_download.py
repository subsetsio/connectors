"""Post-download health invariants for the Reddit connector."""

from subsets_utils import list_raw_files, load_raw_parquet

# Single-file assets (asset id == spec id) vs batched assets (spec-id-NNNN).
_SINGLE = {"reddit-global-activity", "reddit-subreddits"}
_BATCHED = {"reddit-subreddit-subscribers", "reddit-subreddit-activity"}


def test_single_file_assets_nonempty(spec_ids):
    for sid in _SINGLE & set(spec_ids):
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_batched_assets_present_and_nonempty(spec_ids):
    """The per-subreddit assets are written as batch files (<sid>-NNNN.parquet).
    If enumeration broke we'd get zero batches; if a fetch broke, empty rows."""
    for sid in _BATCHED & set(spec_ids):
        files = list_raw_files(f"{sid}-*.parquet")
        assert files, f"{sid}: no batch files found (enumeration likely failed)"
        total = sum(len(load_raw_parquet(f.replace(".parquet", ""))) for f in files)
        assert total > 0, f"{sid}: all {len(files)} batch files are empty"


def test_global_activity_has_all_metrics(spec_ids):
    if "reddit-global-activity" not in spec_ids:
        return
    metrics = set(load_raw_parquet("reddit-global-activity")["metric"].to_pylist())
    expected = {"posts_count", "comments_count", "posts_sum_score", "comments_sum_score"}
    assert expected <= metrics, f"global activity missing metrics: {expected - metrics}"


def test_subscribers_coverage_reasonable(spec_ids):
    """Sanity floor on the flagship table: the >=50k-subscriber universe is
    ~15k subreddits; far fewer means enumeration truncated."""
    sid = "reddit-subreddit-subscribers"
    if sid not in spec_ids:
        return
    names = set()
    for f in list_raw_files(f"{sid}-*.parquet"):
        names.update(load_raw_parquet(f.replace(".parquet", ""))["subreddit"].to_pylist())
    assert len(names) >= 5000, f"{sid}: only {len(names)} subreddits with subscriber series"
