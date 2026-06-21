"""Health invariants for the NASA connector's raw assets.

Exoplanet tables are written as gzipped CSV (`<id>.csv.gz`); the JPL/GISTEMP/
EONET assets are written as NDJSON (`<id>.ndjson.zst`). Tests load each through
the matching subsets_utils path and assert the payload is real, not an empty or
truncated body.
"""

from subsets_utils import list_raw_files, load_raw_ndjson, raw_reader


def test_every_spec_has_a_raw_file(spec_ids):
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        assert files, f"{sid}: no raw file written"


def test_ndjson_assets_nonempty(spec_ids):
    """JPL / GISTEMP / EONET assets must hold rows. Empty usually means the
    endpoint changed shape or the parse silently dropped everything."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        if any(".ndjson" in f for f in files):
            rows = load_raw_ndjson(sid)
            assert len(rows) > 0, f"{sid}: ndjson has 0 rows"
            assert isinstance(rows[0], dict) and rows[0], f"{sid}: empty record"


def test_csv_assets_have_header_and_data(spec_ids):
    """Exoplanet CSV assets must have a comma-delimited header plus >=1 data
    row — guards against a TAP error page or an empty result slipping through."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        if any(".csv" in f for f in files):
            with raw_reader(sid, "csv.gz", mode="rt", compression="gzip") as f:
                header = f.readline()
                first = f.readline()
            assert header and "," in header, f"{sid}: missing CSV header"
            assert first.strip(), f"{sid}: CSV header present but no data rows"
