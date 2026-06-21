"""Health invariants for the Our World in Data connector.

Run post-DAG, in-connector. Catch silent degradation that file-existence alone
misses: empty/truncated payloads, the OWID CSV backbone changing shape.
"""
from subsets_utils import load_raw_parquet, list_raw_files

BACKBONE = {"entity", "year"}  # daily charts use 'day' instead of 'year'


def test_most_charts_have_raw(spec_ids):
    """Nearly every published chart should have produced a raw parquet. A few
    404s (charts unpublished between collect and run) are tolerable, but a large
    shortfall means the Chart API or enumeration broke."""
    present = 0
    for sid in spec_ids:
        if list_raw_files(sid):
            present += 1
    frac = present / max(1, len(spec_ids))
    assert frac >= 0.95, (
        f"only {present}/{len(spec_ids)} charts produced raw ({frac:.1%}); "
        "expected >=95%"
    )


def test_raw_assets_nonempty_and_shaped(spec_ids):
    """Sample raw assets: each should hold rows and carry the OWID backbone
    (entity + a year/day time column). An all-empty or backbone-less table means
    the CSV format changed or we saved an error page."""
    sample = spec_ids[:: max(1, len(spec_ids) // 50)][:50]
    checked = 0
    for sid in sample:
        if not list_raw_files(sid):
            continue  # tolerated 404, covered by the coverage test above
        table = load_raw_parquet(sid)
        assert table.num_rows > 0, f"{sid}: raw parquet has 0 rows"
        cols = {c.lower() for c in table.column_names}
        assert "entity" in cols, f"{sid}: missing 'entity' column, got {sorted(cols)}"
        assert cols & {"year", "day"}, f"{sid}: no year/day time column, got {sorted(cols)}"
        # Beyond the backbone there must be at least one value column.
        assert len(table.column_names) >= 4 or (cols - {"entity", "code", "year", "day"}), (
            f"{sid}: no value column beyond backbone, got {table.column_names}"
        )
        checked += 1
    assert checked > 0, "no sampled raw assets were present to validate"
