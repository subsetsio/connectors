"""Health invariants for The Numbers raw assets.

Charts are written as per-year batch files (`<spec_id>-<year>.parquet`); the
annual table is a single file (`<spec_id>.parquet`). Both are matched by
globbing `<spec_id>*.parquet` — the four spec-id prefixes are distinct, so a
glob never picks up a sibling's files.
"""
from subsets_utils import list_raw_files, load_raw_parquet


def _files_for(spec_id):
    return [f for f in list_raw_files(f"{spec_id}*.parquet")]


def test_raw_assets_nonempty(spec_ids):
    """Each download spec must produce at least one raw parquet with rows.
    Empty payloads usually mean the page layout changed and the table stopped
    matching the header probe."""
    for sid in spec_ids:
        files = _files_for(sid)
        assert files, f"{sid}: no raw parquet files found"
        rows = sum(load_raw_parquet(f[: -len(".parquet")]).num_rows for f in files)
        assert rows > 0, f"{sid}: 0 rows across {len(files)} file(s)"


def test_titles_present(spec_ids):
    """The title column must be populated — a fully-null title column means the
    'Title'/'Movie' header stopped being found and rows were dropped or mangled."""
    for sid in spec_ids:
        files = _files_for(sid)
        if not files:
            continue
        seen = 0
        non_null = 0
        for f in files:
            t = load_raw_parquet(f[: -len(".parquet")])
            if "title" not in t.column_names:
                raise AssertionError(f"{sid}: no 'title' column")
            col = t.column("title")
            seen += len(col)
            non_null += len(col) - col.null_count
        assert seen == 0 or non_null / seen > 0.95, (
            f"{sid}: only {non_null}/{seen} titles non-null"
        )
