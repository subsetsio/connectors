"""Post-DAG health invariants for the StatCounter connector.

These run in-connector after the download nodes, reading raw through the same
loader the nodes wrote with. They catch silent degradation that file existence
alone misses: empty payloads, a region sweep that collapsed to worldwide-only,
or % values that drifted out of range (a format/units change upstream).
"""

from subsets_utils import load_raw_parquet

_RESOLUTION_ID = "statcounter-screen-resolution"


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must have produced rows."""
    for sid in spec_ids:
        table = load_raw_parquet(sid)
        assert len(table) > 0, f"{sid}: raw parquet has 0 rows"


def test_expected_columns(spec_ids):
    """Long-format schema must be intact for each asset kind."""
    ts_cols = {"date", "region_code", "region_name", "region_type", "category", "market_share"}
    res_cols = {"year", "region_code", "region_name", "region_type", "resolution", "market_share"}
    for sid in spec_ids:
        cols = set(load_raw_parquet(sid).column_names)
        expected = res_cols if sid == _RESOLUTION_ID else ts_cols
        assert expected <= cols, f"{sid}: missing columns {expected - cols}"


def test_market_share_in_range(spec_ids):
    """Market-share percentages must sit within [0, 100] (allow a hair over for
    rounding). Values outside that mean the source changed units or format."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        col = load_raw_parquet(sid).column("market_share")
        lo = pc.min(col).as_py()
        hi = pc.max(col).as_py()
        assert lo is not None and lo >= 0, f"{sid}: negative market_share {lo}"
        assert hi is not None and hi <= 100.5, f"{sid}: market_share {hi} > 100"


def test_worldwide_and_multiregion(spec_ids):
    """Time-series assets must include the worldwide series AND more than one
    region — if the region sweep silently collapsed we'd see only 'ww'."""
    import pyarrow.compute as pc
    for sid in spec_ids:
        if sid == _RESOLUTION_ID:
            continue
        codes = load_raw_parquet(sid).column("region_code")
        distinct = pc.count_distinct(codes).as_py()
        has_ww = pc.any(pc.equal(codes, "ww")).as_py()
        assert has_ww, f"{sid}: worldwide ('ww') region missing"
        assert distinct > 1, f"{sid}: only {distinct} region(s); sweep likely collapsed"
