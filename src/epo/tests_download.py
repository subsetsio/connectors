from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw asset should hold rows. An empty payload usually means
    the endpoint changed format or was Cloudflare-challenged."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_value_table_shape(spec_ids):
    """The core time-series asset must carry both metrics and the full long
    table; a collapse means countries.json structure drifted."""
    sid = "epo-patent-applications-grants"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    metrics = {r["metric"] for r in rows}
    assert {"applications", "grants"} <= metrics, f"metrics={metrics}"
    years = {r["year"] for r in rows}
    assert len(years) >= 5, f"only {len(years)} year columns"
    assert len(rows) > 50000, f"only {len(rows)} long-format rows"


def test_reference_assets(spec_ids):
    """Country and field reference tables must keep their full coverage."""
    if "epo-fields" in spec_ids:
        assert len(load_raw_ndjson("epo-fields")) == 35
    if "epo-countries" in spec_ids:
        assert len(load_raw_ndjson("epo-countries")) >= 150
