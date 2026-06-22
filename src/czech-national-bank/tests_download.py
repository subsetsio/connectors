from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every family's NDJSON raw must hold rows. An empty payload means the
    year walk silently skipped every year (endpoint shape changed) or the
    forward combo discovery failed."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_daily_series_have_history(spec_ids):
    """Daily families span many years (exrates back to 1991). If we only got a
    single year (~a few thousand rows) the year loop broke after one year."""
    for sid in spec_ids:
        if sid.endswith("-daily") and "exrates-daily" in sid:
            rows = load_raw_ndjson(sid)
            assert len(rows) > 50000, (
                f"{sid}: only {len(rows)} rows; expected decades of daily fixing"
            )
