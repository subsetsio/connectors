"""In-connector health invariants, run post-DAG against the raw assets."""

from subsets_utils import load_raw_ndjson


def test_raw_assets_nonempty(spec_ids):
    """Every download spec must produce a non-empty raw ndjson. An empty
    payload usually means the orig subdomain started bot-walling or the JSON
    endpoint changed shape."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert len(rows) > 0, f"{sid}: raw ndjson has 0 rows"


def test_poll_readings_have_averages(spec_ids):
    """The corpus must include RCP-average rows, not just raw polls — that's
    the headline series RCP publishes."""
    sid = "realclearpolitics-poll-readings"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    assert any(r.get("reading_type") == "rcp_average" for r in rows), \
        "no rcp_average readings — the average row parse broke"
    assert all(r.get("race_id") is not None for r in rows), \
        "null race_id present in poll readings"


def test_races_unique_ids(spec_ids):
    """The races catalog is one row per race id; duplicates mean an id was
    written twice."""
    sid = "realclearpolitics-races"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    ids = [r["race_id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate race_id in races catalog"
