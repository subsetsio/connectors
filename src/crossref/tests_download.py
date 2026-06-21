"""Health invariants for the Crossref raw downloads.

Run post-DAG, in-connector, through the same subsets_utils loaders the download
nodes used to save — these catch silent degradation (empty payloads, truncated
crawls, schema drift) that mere file-existence checks miss.
"""

from subsets_utils import list_raw_files, load_raw_parquet

_REGISTRIES = ["crossref-funders", "crossref-journals", "crossref-members"]

# Lower bounds well under the observed catalog sizes (funders ~45.7k, journals
# ~166.8k, members ~32.8k) — a crawl that stops short of these truncated.
_REGISTRY_MIN_ROWS = {
    "crossref-funders": 30_000,
    "crossref-journals": 100_000,
    "crossref-members": 20_000,
}


def test_registries_nonempty_and_complete():
    """Each registry parquet should hold roughly its full catalog — a short
    count means cursor paging terminated early or the endpoint changed shape."""
    for sid in _REGISTRIES:
        table = load_raw_parquet(sid)
        assert len(table) >= _REGISTRY_MIN_ROWS[sid], (
            f"{sid}: {len(table)} rows, expected >= {_REGISTRY_MIN_ROWS[sid]}"
        )


def test_registry_key_columns_present():
    """The columns the transforms select must exist (schema-drift guard)."""
    expected = {
        "crossref-funders": {"funder_id", "name"},
        "crossref-journals": {"title", "issn"},
        "crossref-members": {"member_id", "primary_name"},
    }
    for sid, cols in expected.items():
        names = set(load_raw_parquet(sid).column_names)
        assert cols <= names, f"{sid}: missing columns {cols - names}"


def test_works_batches_present_and_nonempty():
    """The /works firehose writes per-index-date parquet batches; at least one
    batch should exist and carry rows. (Backfill is supervisor-bounded, so we
    assert progress, not full completion.)"""
    batches = list_raw_files("crossref-works-*.parquet")
    assert batches, "no crossref-works-* batch files written"
    total = sum(len(load_raw_parquet(b[: -len(".parquet")])) for b in batches)
    assert total > 0, "crossref-works batches present but hold 0 rows"
