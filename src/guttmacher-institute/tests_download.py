"""Health invariants for the Guttmacher OSF download nodes.

Each node saves its primary public-use table as a raw .csv file. These tests
catch silent degradation that file-existence alone misses: an empty/truncated
download, or an OSF response that switched to an HTML error page instead of
CSV bytes.
"""
from subsets_utils import load_raw_file


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw CSV must hold a header plus at least one data row."""
    for sid in spec_ids:
        text = load_raw_file(sid, extension="csv")
        lines = [ln for ln in text.splitlines() if ln.strip()]
        assert len(lines) >= 2, f"{sid}: raw csv has <2 non-empty lines ({len(lines)})"


def test_raw_looks_like_csv(spec_ids):
    """The first line should be a comma-delimited header, not an HTML/JSON
    error body returned in place of the file."""
    for sid in spec_ids:
        text = load_raw_file(sid, extension="csv")
        header = text.splitlines()[0] if text else ""
        low = header.lstrip().lower()
        assert not low.startswith(("<", "{")), f"{sid}: raw csv header looks like HTML/JSON: {header[:80]!r}"
        assert "," in header, f"{sid}: raw csv header has no comma delimiter: {header[:80]!r}"
