"""Health invariants for the GH Archive download stage.

Raw is written as one immutable parquet batch per UTC day
(gh-archive-github-events-daily-YYYY-MM-DD.parquet), so we discover the batch
files with list_raw_files and load a sample through the same parquet loader the
download node used."""
from subsets_utils import list_raw_files, load_raw_parquet

_ASSET = "gh-archive-github-events-daily"

_KNOWN_TYPES = {
    "PushEvent", "PullRequestEvent", "IssuesEvent", "WatchEvent", "ForkEvent",
    "CreateEvent", "DeleteEvent", "IssueCommentEvent", "PullRequestReviewEvent",
    "PullRequestReviewCommentEvent", "CommitCommentEvent", "GollumEvent",
    "MemberEvent", "PublicEvent", "ReleaseEvent", "SponsorshipEvent",
    "DiscussionEvent", "DiscussionCommentEvent",
}


def _batch_asset_ids():
    files = list_raw_files(f"{_ASSET}-*.parquet")
    return [f[: -len(".parquet")] for f in files]


def test_daily_batches_exist():
    """At least one day must have been processed; zero batches means the
    crawl wrote nothing (URL pattern broke, or every hour 404'd)."""
    ids = _batch_asset_ids()
    assert ids, f"no daily batch files matched {_ASSET}-*.parquet"


def test_batches_nonempty_and_well_formed():
    """Each daily batch holds positive per-type counts for exactly its own
    day, with recognizable GitHub event types. Catches truncated downloads
    and silent format/schema drift."""
    ids = _batch_asset_ids()
    # Sample head + tail so a recent format change is also caught, without
    # loading every batch.
    sample = ids[:3] + ids[-3:]
    for sid in sample:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: empty batch"
        cols = set(table.column_names)
        assert {"date", "event_type", "event_count"} <= cols, f"{sid}: missing columns ({cols})"

        dates = set(table.column("date").to_pylist())
        assert len(dates) == 1, f"{sid}: batch spans multiple dates {dates}"

        counts = table.column("event_count").to_pylist()
        assert all(c > 0 for c in counts), f"{sid}: non-positive event_count present"

        types = set(table.column("event_type").to_pylist())
        assert types & _KNOWN_TYPES, f"{sid}: no recognized GitHub event types in {types}"
