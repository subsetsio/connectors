"""Health-invariant tests for SAMHSA raw download assets.

These run post-DAG, in-connector, reading raw through subsets_utils loaders so
they behave identically locally and in the cloud. They catch silent
degradation that file-existence alone misses: empty payloads, a collapsed
state iteration, a format switch.
"""

from subsets_utils import load_raw_ndjson


def test_all_raw_assets_nonempty(spec_ids):
    """Every download asset must hold rows. Empty usually means the endpoint
    switched format, the WAF kicked in, or pagination broke after page 1."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_findtreatment_national_coverage(spec_ids):
    """The locator is iterated over every state id; a national pull should
    span the full ~24.7k facilities across 50+ states/territories. A large
    drop means the state-id iteration silently collapsed to one state."""
    sid = "samhsa-findtreatment-facilities"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    assert len(rows) >= 15000, f"{sid}: only {len(rows)} facilities (expected ~24.7k)"
    states = {r.get("state") for r in rows if r.get("state")}
    assert len(states) >= 50, f"{sid}: only {len(states)} states (expected 50+)"


def test_synar_shape(spec_ids):
    """Synar is a single bounded dataset (~1,122 rows, 1997-2018). A big
    shortfall means the Socrata pull was truncated or the id changed."""
    sid = "samhsa-escb-scz6"
    if sid not in spec_ids:
        return
    rows = load_raw_ndjson(sid)
    assert len(rows) >= 800, f"{sid}: only {len(rows)} rows (expected ~1,122)"
    assert "data_value" in rows[0], f"{sid}: missing data_value field: {list(rows[0])}"
    assert "ffy_year" in rows[0], f"{sid}: missing ffy_year field: {list(rows[0])}"
