from subsets_utils import load_raw_parquet

EXPECTED_REGIONS = {"Global", "Northern Hemisphere", "Southern Hemisphere"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw parquet should hold rows. Empty means the endpoint
    switched format / version path 404'd silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_three_regions_present(spec_ids):
    """Each cadence combines 3 region CSVs; a missing region means one of the
    per-region fetches silently produced nothing."""
    for sid in spec_ids:
        regions = set(load_raw_parquet(sid).column("region").to_pylist())
        assert regions == EXPECTED_REGIONS, f"{sid}: regions={regions}"


def test_anomalies_in_physical_range(spec_ids):
    """Anomalies are deg C vs 1961-1990; sanity-bound to catch parse/scale
    errors (e.g. a column shift would push values far outside [-5, 5])."""
    for sid in spec_ids:
        vals = [v for v in load_raw_parquet(sid).column("anomaly_c").to_pylist() if v is not None]
        assert vals, f"{sid}: no non-null anomalies"
        assert all(-5.0 < v < 5.0 for v in vals), f"{sid}: anomaly out of range"
