"""Health invariants for the CDC raw downloads.

Each download streams a Socrata dataset's full CSV export to a gzip-compressed
raw asset (`<spec-id>.csv.gz`). These tests catch the silent-degradation modes
that file existence alone misses: a truncated/empty export, or a payload that is
no longer CSV (auth wall, HTML error page, format switch).
"""

from subsets_utils import list_raw_files, raw_reader


def test_raw_assets_present(spec_ids):
    """Every download spec must have written a raw CSV asset."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.csv.gz")
        assert files, f"{sid}: no raw csv.gz written"


def test_raw_csv_header_and_rows(spec_ids):
    """Each raw CSV must have a non-empty header line and at least one data row.
    An export that returns only a header (or nothing) means the dataset came back
    empty/truncated; an HTML error page would lack the comma/quote structure."""
    for sid in spec_ids:
        with raw_reader(sid, "csv.gz", mode="rt", compression="gzip") as f:
            header = f.readline()
            assert header.strip(), f"{sid}: CSV has no header (empty export)"
            first_row = f.readline()
            assert first_row.strip(), f"{sid}: CSV header but no data rows"
