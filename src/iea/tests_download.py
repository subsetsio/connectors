"""Health-invariant tests for the IEA connector raw assets.

Run post-DAG, in-connector, through subsets_utils loaders — identical behaviour
locally and in the cloud.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every indicator's raw NDJSON must hold rows. An empty payload means the
    /stats/indicator endpoint changed shape or returned an error envelope."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_expected_keys_present(spec_ids):
    """Each row must carry the long-format keys the transform CASTs. A missing
    key signals an upstream schema change the transform would silently null."""
    required = {"year", "country", "short", "flow", "product", "value", "units"}
    for sid in spec_ids:
        if sid == "iea-countries":
            continue
        rows = load_raw_ndjson(sid)
        sample = rows[0]
        missing = required - set(sample.keys())
        assert not missing, f"{sid}: rows missing expected keys {missing}"


def test_has_real_values(spec_ids):
    """At least some non-null numeric values per indicator — guards against a
    response that is all-null (e.g. a soft error returning a stub series)."""
    for sid in spec_ids:
        if sid == "iea-countries":
            continue
        rows = load_raw_ndjson(sid)
        non_null = sum(1 for r in rows if r.get("value") is not None)
        assert non_null > 0, f"{sid}: every value is null ({len(rows)} rows)"


def test_countries_shape(spec_ids):
    if "iea-countries" not in spec_ids:
        return
    rows = load_raw_ndjson("iea-countries")
    required = {"name", "stats", "isRegion", "regions"}
    missing = required - set(rows[0].keys())
    assert not missing, f"iea-countries: rows missing expected keys {missing}"
    assert len(rows) >= 150, f"iea-countries: expected at least 150 rows, got {len(rows)}"
