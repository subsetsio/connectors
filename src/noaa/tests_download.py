"""Post-DAG health invariants for the NOAA connector raw assets."""

from subsets_utils import load_raw_parquet


def test_all_assets_nonempty(spec_ids):
    """Every download asset must hold rows — an empty payload means the listing
    parse broke, the file moved, or the format changed silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_storm_events_volume(spec_ids):
    """Storm Events spans 1950..present across ~75 yearly files; a sharp drop
    means yearly-file discovery silently truncated."""
    sid = "noaa-storm-events"
    if sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 500000, f"storm-events only {len(table)} rows; expected >500k"


def test_ibtracs_volume(spec_ids):
    """IBTrACS ALL holds ~700k 3-hourly track points; <100k means the units-row
    skip or column selection broke."""
    sid = "noaa-international-best-track-archive-for-climate-stewardship-ibtracs"
    if sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 100000, f"ibtracs only {len(table)} rows; expected >100k"
