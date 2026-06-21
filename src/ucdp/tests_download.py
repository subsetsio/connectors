"""Health invariants for UCDP raw assets.

Each download node writes one parquet snapshot of a full UCDP dataset. These
checks catch silent degradation the file-exists check misses: empty/truncated
payloads, a download that switched to an error page, or a zip member that
parsed to zero rows.
"""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every dataset must hold rows — UCDP files are never empty."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"


def test_all_raw_assets_have_columns(spec_ids):
    """A real UCDP table has many columns; 0/1 columns means a parse fell back
    to treating the whole line as one field (wrong delimiter / HTML error page)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert table.num_columns >= 3, (
            f"{sid}: only {table.num_columns} column(s) — likely a delimiter "
            f"or download failure"
        )


def test_ged_is_large(spec_ids):
    """The flagship Georeferenced Event Dataset is event-level with hundreds of
    thousands of rows; a tiny GED means a truncated download."""
    if "ucdp-ged" in spec_ids:
        table = load_raw_parquet("ucdp-ged")
        assert table.num_rows > 100_000, f"ucdp-ged: only {table.num_rows} rows"
