"""Health invariants for the Hugging Face Hub raw assets.

Catches silent degradation that file existence alone misses — a missing asset,
an empty payload, or the daily-papers feed switching shape. The large list
assets (models/datasets/spaces) are millions of rows, so we check for file
presence rather than loading them whole; the small daily-papers asset is loaded
and inspected directly.
"""

from subsets_utils import list_raw_files, load_raw_ndjson


def test_all_raw_assets_present(spec_ids):
    """Every download spec must produce at least one raw file."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        assert files, f"{sid}: no raw file produced (glob '{sid}.*' empty)"


def test_daily_papers_nonempty_and_shaped(spec_ids):
    """The small daily-papers feed should hold rows with the flattened paper id."""
    sid = "hugging-face-hub-daily-papers"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"
    assert any(r.get("paper_id") for r in rows[:50]), f"{sid}: no paper_id in first rows — feed shape changed"
