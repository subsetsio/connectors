"""Health-invariant tests for DBT raw downloads.

Each download node saves its raw payload as a CSV file via save_raw_file, so
we load it back the same way and assert it isn't empty/degraded. Empty or
near-empty payloads usually mean the data endpoint switched format, the
`latest` redirect broke, or the source returned an error page in place of data.
"""

from subsets_utils import load_raw_file


def _download_ids(spec_ids):
    """spec_ids carries both download and transform node ids; only download
    nodes write a raw CSV, so the SQL-transform leaves are filtered out."""
    return [s for s in spec_ids if not s.endswith("-transform")]


def test_all_raw_assets_present_and_nonempty(spec_ids):
    """Every download spec's raw CSV should exist and carry a header plus rows."""
    for sid in _download_ids(spec_ids):
        text = load_raw_file(sid, extension="csv")
        assert isinstance(text, str) and text, f"{sid}: raw csv empty/undecodable"
        # header line + at least one data row
        nl = text.find("\n")
        assert nl != -1 and len(text) > nl + 1, f"{sid}: csv has no data rows"


def test_no_html_error_page(spec_ids):
    """A failed fetch can return an S3/HTML error doc with a 200; guard so a
    transform never silently reads an error page as data."""
    for sid in _download_ids(spec_ids):
        head = load_raw_file(sid, extension="csv")[:200].lstrip().lower()
        assert not head.startswith("<?xml"), f"{sid}: looks like an XML error doc"
        assert not head.startswith("<!doctype"), f"{sid}: looks like an HTML page"
        assert not head.startswith("<html"), f"{sid}: looks like an HTML page"
