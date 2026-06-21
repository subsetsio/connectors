"""Health-invariant tests for the PSMSL connector raw assets."""

from subsets_utils import load_raw_parquet


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec's raw asset must hold rows — empty means the ZIP
    download or the per-station parse silently broke. Transform specs publish
    Delta tables (not raw parquet), so they are excluded."""
    download_ids = [sid for sid in spec_ids if not sid.endswith("-transform")]
    for sid in download_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_stations_catalog_reasonable(spec_ids):
    """The station catalog should list ~thousands of gauges; a tiny count means
    filelist.txt was not found or parsed."""
    table = load_raw_parquet("psmsl-stations")
    assert len(table) >= 1000, f"stations: only {len(table)} rows (<1000)"
    cols = set(table.column_names)
    assert {"station_id", "latitude", "longitude"} <= cols, f"missing cols: {cols}"


def test_rlr_monthly_shape(spec_ids):
    """RLR monthly should carry many station-months with plausible MSL and a
    derived month in 1..12."""
    table = load_raw_parquet("psmsl-rlr-monthly")
    assert len(table) >= 100_000, f"rlr-monthly: only {len(table)} rows"
    months = set(table.column("month").to_pylist()[:5000])
    assert months <= set(range(1, 13)), f"month out of range: {sorted(months)}"
    # MSL in mm relative to RLR datum clusters around ~7000; sanity-bound it.
    vals = [v for v in table.column("msl_mm").to_pylist()[:5000] if v is not None]
    assert vals, "rlr-monthly: no non-null msl_mm in sample"
    assert all(-50_000 < v < 50_000 for v in vals), "implausible msl_mm values"
