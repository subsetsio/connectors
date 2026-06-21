"""Post-DAG health invariants for the ARCEP connector.

These run in-connector after the download nodes, reading raw through the same
subsets_utils loader the fetch fn used (NDJSON). They catch silent degradation
that file-existence alone misses: an endpoint that started returning an HTML
directory listing, a format switch that yields a header-only file, etc.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every family asset must hold rows. Zero rows usually means the resource
    URL started redirecting to a directory listing or the CSV format changed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw NDJSON has 0 rows"


def test_no_html_leaked(spec_ids):
    """A directory listing or error page parsed as CSV shows up as a row whose
    first value contains an HTML tag. Guard against it explicitly."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[: min(50, len(rows))]
        for rec in sample:
            blob = " ".join(str(v) for v in rec.values() if v).lower()
            assert "<!doctype" not in blob and "<html" not in blob, (
                f"{sid}: HTML content leaked into rows — resource resolved to a page, not a CSV"
            )


def test_provenance_columns_present(spec_ids):
    """Every row carries the provenance columns the fetch fn stamps on."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert "_resource_title" in rows[0], f"{sid}: missing _resource_title column"
