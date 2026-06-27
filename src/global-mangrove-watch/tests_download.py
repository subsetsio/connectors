"""Health-invariant tests run post-DAG, in-connector, against the raw assets."""
from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download spec must produce a non-empty raw ndjson. An empty payload
    means the widget/locations endpoint changed shape or the host moved."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_widgets_have_location_identity(spec_ids):
    """Every widget row carries a location identity (location_id + type). The
    locations catalog uses `id` instead, so it is exempt."""
    for sid in spec_ids:
        if sid.endswith("-locations"):
            continue
        rows = load_raw_ndjson(sid)
        bad = [r for r in rows[:5000] if r.get("location_id") is None
               or r.get("location_type") not in ("country", "worldwide")]
        assert not bad, f"{sid}: {len(bad)} rows missing/!invalid location identity"


def test_locations_catalog_complete(spec_ids):
    """The locations catalog must enumerate the full set (countries + WDPA +
    worldwide, ~3124); far fewer means pagination/format broke."""
    sid = "global-mangrove-watch-locations"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    assert len(rows) >= 3000, f"{sid}: only {len(rows)} locations, expected >=3000"
    types = {r.get("location_type") for r in rows}
    assert {"country", "wdpa", "worldwide"} <= types, f"missing types: {types}"
