"""Health-invariant tests for the FEC connector's raw assets.

Some assets are written as a single parquet (`<id>.parquet`), others as
per-cycle batches (`<id>-<cycle>-<seq>.parquet`). Resolve both via the same
glob the SQL transform runtime uses.
"""

import duckdb

from subsets_utils import list_raw_files
from subsets_utils.config import raw_uri

# Streamed (batched) downloads vs. single-file downloads.
_BATCHED = {
    "fec-individual-contributions",
    "fec-inter-committee-transactions",
    "fec-operating-expenditures",
    "fec-pac-contributions",
}


def _raw_paths(sid):
    rels = list_raw_files(f"{sid}.parquet") or list_raw_files(f"{sid}-*.parquet")
    base = raw_uri("__probe__", "__").rsplit("/", 1)[0]
    return rels, [f"{base}/{rel}" for rel in rels]


def test_every_asset_has_files(spec_ids):
    """Each download spec must have produced at least one raw parquet file."""
    for sid in spec_ids:
        rels, _ = _raw_paths(sid)
        assert rels, f"{sid}: no raw parquet files found"


def test_every_asset_nonempty(spec_ids):
    """Every raw asset must hold rows — empty payloads mean a download or
    format change broke silently."""
    for sid in spec_ids:
        _, paths = _raw_paths(sid)
        n = duckdb.sql(f"SELECT count(*) FROM read_parquet({paths})").fetchone()[0]
        assert n > 0, f"{sid}: raw parquet has 0 rows"


def test_has_cycle_column(spec_ids):
    """Every raw asset carries the cycle partition column with 4-digit years."""
    for sid in spec_ids:
        _, paths = _raw_paths(sid)
        cycles = duckdb.sql(
            f"SELECT DISTINCT cycle FROM read_parquet({paths}) LIMIT 50"
        ).fetchall()
        vals = [c[0] for c in cycles]
        assert vals, f"{sid}: no cycle values"
        for v in vals:
            assert v and len(str(v)) == 4 and str(v).isdigit(), \
                f"{sid}: bad cycle value {v!r}"


def test_large_tables_have_volume(spec_ids):
    """The itemized transaction tables should be large; a tiny count means a
    streamed cycle silently truncated."""
    expectations = {
        "fec-individual-contributions": 1_000_000,
        "fec-pac-contributions": 50_000,
        "fec-operating-expenditures": 50_000,
        "fec-inter-committee-transactions": 50_000,
    }
    for sid, floor in expectations.items():
        if sid not in spec_ids:
            continue
        _, paths = _raw_paths(sid)
        n = duckdb.sql(f"SELECT count(*) FROM read_parquet({paths})").fetchone()[0]
        assert n >= floor, f"{sid}: only {n:,} rows, expected >= {floor:,}"
