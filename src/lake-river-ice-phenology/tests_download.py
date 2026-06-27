from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw NDJSON should hold rows. An empty payload usually means
    the NSIDC endpoint changed format or the download was truncated."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_freeze_thaw_has_expected_columns(spec_ids):
    """Guard against an upstream header change silently reshaping the CSV."""
    sid = "lake-river-ice-phenology-freeze-thaw"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    required = {"lakecode", "season", "iceon_year", "iceoff_year", "froze"}
    missing = required - set(rows[0].keys())
    assert not missing, f"{sid}: missing expected columns {missing}"


def test_physical_has_expected_columns(spec_ids):
    sid = "lake-river-ice-phenology-physical-characteristics"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    required = {"lakecode", "lat_decimal", "lon_decimal", "surface_area"}
    missing = required - set(rows[0].keys())
    assert not missing, f"{sid}: missing expected columns {missing}"
