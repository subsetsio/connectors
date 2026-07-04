"""Health invariants for the NASA connector's raw assets.

Exoplanet TAP tables are written as typed parquet (`<id>.parquet`); the JPL/
GISTEMP/EONET assets are written as NDJSON (`<id>.ndjson.zst`). Tests load each
through the matching subsets_utils path and assert the payload is real, not an
empty or truncated body.
"""

from subsets_utils import list_raw_files, load_raw_ndjson, load_raw_parquet


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


def test_parquet_assets_nonempty_and_wide(spec_ids):
    """Exoplanet parquet assets must hold rows and their full column sets —
    guards against a TAP error page or a truncated dump slipping through."""
    for sid in spec_ids:
        files = list_raw_files(f"{sid}.*")
        if any(f.endswith(".parquet") for f in files):
            table = load_raw_parquet(sid)
            assert table.num_rows > 0, f"{sid}: parquet has 0 rows"
            assert table.num_columns >= 80, (
                f"{sid}: only {table.num_columns} columns — TAP dump truncated?"
            )
