"""In-connector health-invariant tests, run post-DAG against the raw assets."""
from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Empty raw usually means the EML hash resolution or the CSV download
    silently broke (wrong revision, redirect to an error page)."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_measurements_have_clarity(spec_ids):
    """The flagship table must carry the Secchi clarity column with real
    (non-null) readings -- the whole point of this connector."""
    sid = "lagos-ne-in-situ-measurements-of-epilimnetic-nutrients-and-secchi-data"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    assert "secchi" in table.column_names, "measurements missing 'secchi' column"
    col = table.column("secchi")
    assert (col.length() - col.null_count) > 0, "no non-null secchi readings"


def test_morphometry_has_coords(spec_ids):
    """The lake reference table must carry usable lat/long coordinates."""
    sid = "lagos-ne-lake-identifiers-and-morphometry"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    for c in ("lagoslakeid", "nhd_lat", "nhd_long"):
        assert c in table.column_names, f"morphometry missing '{c}' column"
