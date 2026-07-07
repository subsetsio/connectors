"""Health invariants for SOCAT raw CSV downloads."""

from subsets_utils import list_raw_files, raw_reader


def test_raw_assets_present(spec_ids):
    for spec_id in spec_ids:
        files = list_raw_files(f"{spec_id}.csv.gz")
        assert files, f"{spec_id}: no raw csv.gz file written"


def test_raw_csv_header_and_rows(spec_ids):
    for spec_id in spec_ids:
        with raw_reader(spec_id, "csv.gz", mode="rt", compression="gzip") as handle:
            header = handle.readline()
            assert header.strip(), f"{spec_id}: empty CSV header"
            first = handle.readline()
            second = handle.readline()
            assert first.strip() or second.strip(), f"{spec_id}: CSV has no rows after header"
            assert "," in header, f"{spec_id}: header does not look comma-delimited"
