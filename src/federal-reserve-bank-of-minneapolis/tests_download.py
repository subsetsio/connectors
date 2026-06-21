"""Health-invariant tests for the Minneapolis Fed connector.

Run post-DAG, in-connector, against the raw assets each download node wrote.
They catch silent degradation that file-existence alone misses: a variant CSV
that 404'd and got dropped from the union, an empty scrape, a schema change.
"""

from subsets_utils import load_raw_parquet

# Minimum rows expected per raw asset (roughly half of what was observed at
# authoring time, so normal fluctuation passes but a dropped variant trips it).
MIN_ROWS = {
    "federal-reserve-bank-of-minneapolis-pctl-of-inc": 50_000,
    "federal-reserve-bank-of-minneapolis-inc-share": 300_000,
    "federal-reserve-bank-of-minneapolis-prop-share": 150_000,
    "federal-reserve-bank-of-minneapolis-inc-change-distributions": 1_000_000,
    "federal-reserve-bank-of-minneapolis-transition-matrix": 1_000_000,
    "federal-reserve-bank-of-minneapolis-cpi-historical": 300,
}


def test_all_raw_assets_meet_min_rows(spec_ids):
    """Every raw asset should clear its expected floor. A short table usually
    means one of the unioned source files failed to load silently."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        floor = MIN_ROWS.get(sid, 1)
        assert len(table) >= floor, f"{sid}: {len(table)} rows < expected {floor}"


def test_idda_geography_coverage(spec_ids):
    """Each IDDA module must include both the national/state universe and the
    native-area universe — i.e. the na_* file was unioned in, not dropped."""
    for sid in spec_ids:
        if sid == "federal-reserve-bank-of-minneapolis-cpi-historical":
            continue
        table = load_raw_parquet(sid)
        geos = set(table.column("geo_var").to_pylist())
        assert "native_areas" in geos, f"{sid}: native_areas missing — na_* file not unioned ({geos})"
        assert geos & {"usst", "state"}, f"{sid}: no US/state rows ({geos})"


def test_cpi_has_both_series(spec_ids):
    """The CPI scrape must carry both historical tables."""
    sid = "federal-reserve-bank-of-minneapolis-cpi-historical"
    if sid not in spec_ids:
        return
    table = load_raw_parquet(sid)
    series = set(table.column("series").to_pylist())
    assert series == {"cpi_1800", "cpi_1913"}, f"{sid}: unexpected series set {series}"
