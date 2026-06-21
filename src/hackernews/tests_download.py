"""Health invariants for the Hacker News items firehose.

The download writes id-range batches as ``hackernews-items-{lo}-{hi}.parquet``.
These tests catch silent degradation a file-existence check misses: no batches
written at all, empty/format-broken batches, or a batch that lost the core
columns (endpoint switched shape).
"""

from subsets_utils import list_raw_files, load_raw_parquet

_CORE_COLUMNS = {"id", "type", "by", "time"}


def test_item_batches_written(spec_ids):
    """At least one id-range batch must exist — otherwise the crawl produced
    nothing (max-item lookup or per-item fetch silently failed)."""
    batches = list_raw_files("hackernews-items-*.parquet")
    assert batches, "no hackernews-items-*.parquet batch files were written"


def test_batches_nonempty_and_typed():
    """Every batch holds rows and carries the core columns with sane ids.
    Empty payloads or missing columns mean the endpoint shape changed."""
    batches = list_raw_files("hackernews-items-*.parquet")
    assert batches, "no batch files to check"
    for rel in batches:
        asset = rel[: -len(".parquet")]
        table = load_raw_parquet(asset)
        assert table.num_rows > 0, f"{asset}: 0 rows"
        missing = _CORE_COLUMNS - set(table.column_names)
        assert not missing, f"{asset}: missing core columns {missing}"
        ids = table.column("id").to_pylist()
        assert all(i is not None for i in ids), f"{asset}: null id present"
        types = set(table.column("type").to_pylist())
        assert types <= {"story", "comment", "job", "poll", "pollopt"}, \
            f"{asset}: unexpected item types {types - {'story','comment','job','poll','pollopt'}}"
