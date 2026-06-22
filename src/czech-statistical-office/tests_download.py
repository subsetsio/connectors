"""Health-invariant tests for the czech-statistical-office connector.

Each download node saves the dataset's raw CSV verbatim via `save_raw_file`.
These tests reload through the same loader and assert the download is a real,
non-empty CSV — catching silent degradation (empty payloads, truncated bodies,
an endpoint that switched format) that file-existence alone would miss.
"""

from subsets_utils import load_raw_file


def test_all_raw_assets_nonempty_csv(spec_ids):
    """Every spec's raw CSV should be non-empty and carry a header row with at
    least one delimiter — an empty body or an HTML error page slipping through
    means the endpoint changed format or the download truncated."""
    for sid in spec_ids:
        content = load_raw_file(sid, extension="csv", binary=True)
        assert content, f"{sid}: raw CSV is empty"
        head = content[:4096].decode("utf-8", errors="replace").lstrip("﻿")
        first_line = head.splitlines()[0] if head.splitlines() else ""
        assert "," in first_line, (
            f"{sid}: first line has no comma delimiter; "
            f"got {first_line[:120]!r} (format may have changed)"
        )
        assert "<html" not in head.lower(), (
            f"{sid}: raw body looks like HTML, not CSV"
        )
