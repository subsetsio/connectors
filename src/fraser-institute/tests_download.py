"""Post-DAG health invariants for the Fraser Institute raw assets."""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every endpoint returns thousands of jurisdiction-year rows. An empty or
    tiny payload means the endpoint changed shape or the JSON envelope moved."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) >= 1000, f"{sid}: only {len(rows)} raw rows (expected >=1000)"


def test_core_fields_present(spec_ids):
    """Every flattened row must carry the join keys (year, iso_code) and the
    headline index value; their absence means the flatten or source drifted."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        for field in ("year", "iso_code", "summary_index"):
            assert field in sample, f"{sid}: row missing '{field}': keys={sorted(sample)}"


def test_area_columns_present(spec_ids):
    """Each index is built from area sub-scores flattened to area1.. columns; if
    they vanished the Area {label,value} objects stopped being flattened."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        area_cols = [k for k in sample if k.startswith("area")]
        assert len(area_cols) >= 3, f"{sid}: only {len(area_cols)} area columns"
