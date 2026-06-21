"""Post-DAG health invariants for the Rosstat connector.

Raw is written as wide NDJSON (one object per data row). These tests catch
silent degradation that file-existence alone misses: empty payloads, the portal
returning an HTML soft-404 instead of data, or a decode regression that wipes a
file's columns.
"""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset's normalized NDJSON must hold at least one row. An empty
    file means the data URL stopped resolving or the source switched format."""
    empties = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            empties.append(sid)
    assert not empties, f"raw NDJSON empty for: {empties}"


def test_rows_have_columns(spec_ids):
    """Each row should be a non-empty object. A row that decoded to {} means the
    header parse collapsed (wrong delimiter, lost preamble handling)."""
    bad = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if rows and not any(isinstance(r, dict) and len(r) >= 1 for r in rows[:5]):
            bad.append(sid)
    assert not bad, f"rows carry no columns for: {bad}"


def test_no_html_leaked(spec_ids):
    """The portal serves a generic HTML shell on soft-404. If that leaked into a
    data file, the first row's keys would look like HTML tags, not field names."""
    suspect = []
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        if not rows:
            continue
        keys = " ".join(str(k) for k in rows[0].keys()).lower()
        if "<!doctype" in keys or "<html" in keys or "<head" in keys:
            suspect.append(sid)
    assert not suspect, f"HTML leaked into raw for: {suspect}"
