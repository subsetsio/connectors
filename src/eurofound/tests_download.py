from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows; an empty payload means the CDN file
    moved or the xlsx sheet name changed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_rates_volume(spec_ids):
    """The Rates sheet is the bulk of the value (~198k obs). A small count means
    the sheet read truncated after the header block."""
    sid = "eurofound-collectively-agreed-wages-rates"
    if sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 50000, f"{sid}: only {len(rows)} rows, expected ~198k"
