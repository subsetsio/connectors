"""Health-invariant tests for METI raw assets."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Each accepted entity must produce SQL-readable discovery or table rows."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw NDJSON has 0 rows"


def test_each_asset_has_source_links(spec_ids):
    """Every asset should at least record the METI page/file links it used."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        link_rows = [r for r in rows if r.get("kind") in {"page", "file"}]
        assert link_rows, f"{sid}: no page/file provenance rows found"


def test_downloaded_rows_have_values_when_present(spec_ids):
    """Workbook/CSV table rows must carry a values array, not only metadata."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        table_rows = [r for r in rows if r.get("kind") == "row"]
        for row in table_rows[:100]:
            values = row.get("values")
            assert isinstance(values, list) and any(v is not None for v in values), (
                f"{sid}: malformed table row {row}"
            )
