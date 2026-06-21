"""Post-DAG health invariants for the FCC connector.

Each raw asset is a gzip-compressed CSV streamed from the Socrata export. A
truncated download or a silently-changed endpoint usually shows up as a missing
file, an empty body, or a header with no data rows — these tests catch that
without touching the filesystem directly.
"""
from subsets_utils import raw_reader, list_raw_files


def test_all_raw_assets_present_and_have_rows(spec_ids):
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        assert files, f"{sid}: no raw file written"
        with raw_reader(sid, extension="csv.gz", mode="rt",
                        compression="gzip") as f:
            header = f.readline()
            assert header.strip(), f"{sid}: empty CSV (no header)"
            first_row = f.readline()
            assert first_row.strip(), f"{sid}: CSV has a header but no data rows"
