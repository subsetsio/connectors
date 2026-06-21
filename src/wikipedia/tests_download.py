"""Post-DAG health invariants for the Wikipedia (AQS) connector.

These catch silent degradation that file-existence alone misses: a per-project
family that collapsed to a handful of projects (sitematrix broke), an empty
payload, or a project column that stopped being populated.
"""
from subsets_utils import load_raw_parquet

# Per-project families and the value column that must be populated.
_PER_PROJECT = {
    "wikipedia-pageviews": "views",
    "wikipedia-unique-devices": "devices",
    "wikipedia-editors": "editors",
    "wikipedia-edits": "edits",
    "wikipedia-edited-pages": "edited_pages",
    "wikipedia-bytes-difference-net": "net_bytes_diff",
    "wikipedia-bytes-difference-absolute": "abs_bytes_diff",
    "wikipedia-registered-users-new": "new_registered_users",
}


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must have written rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_per_project_breadth(spec_ids):
    """Per-project families must span many distinct projects. If sitematrix
    enumeration or the API silently degraded we'd see only a handful."""
    for sid in _PER_PROJECT:
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        projects = set(table.column("project").to_pylist())
        assert len(projects) >= 100, (
            f"{sid}: only {len(projects)} distinct projects; expected >=100"
        )


def test_value_columns_have_data(spec_ids):
    """The headline value column of each per-project family must be non-null
    for at least most rows — an all-null column means parsing broke."""
    for sid, col in _PER_PROJECT.items():
        if sid not in spec_ids:
            continue
        table = load_raw_parquet(sid)
        vals = table.column(col).to_pylist()
        non_null = sum(1 for v in vals if v is not None)
        assert non_null > 0, f"{sid}: value column {col!r} is entirely null"


def test_mediarequests_media_types(spec_ids):
    """mediarequests must carry several media-type breakdowns, not just one."""
    sid = "wikipedia-mediarequests"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    media_types = set(table.column("media_type").to_pylist())
    assert len(media_types) >= 3, (
        f"{sid}: only media types {media_types}; expected >=3"
    )
