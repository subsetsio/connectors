"""Health invariants run post-DAG, in-connector, against the raw NDJSON assets.

These catch silent degradation that file-existence misses: empty payloads,
the per-season pager dropping every season, or gameTypeId injection failing.
"""

from subsets_utils import load_raw_ndjson
from constants import ENTITY_FETCH


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw NDJSON should hold rows. Empty = endpoint changed
    shape, auth/path broke, or the season pager returned nothing."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_reports_have_seasonid_and_gametype(spec_ids):
    """Report rows must carry seasonId (from the source) and gameTypeId (which
    we inject — its absence means injection silently broke)."""
    for sid in spec_ids:
        entity_id = sid[len("nhl-api-"):]
        kind, _ = ENTITY_FETCH.get(entity_id, ("reference", None))
        if kind != "report":
            continue
        row = load_raw_ndjson(sid)[0]
        assert "seasonId" in row, f"{sid}: row missing seasonId: {sorted(row)[:8]}"
        assert "gameTypeId" in row, f"{sid}: row missing injected gameTypeId"
        assert row["gameTypeId"] in (2, 3), f"{sid}: bad gameTypeId {row['gameTypeId']}"


def test_reports_span_many_seasons(spec_ids):
    """A core report (skater/goalie/team summary) covers the full league
    history; if the pager broke after one season we'd see ~1 distinct season."""
    for sid in ("nhl-api-skater-summary", "nhl-api-goalie-summary", "nhl-api-team-summary"):
        if sid not in spec_ids:
            continue
        seasons = {r["seasonId"] for r in load_raw_ndjson(sid)}
        assert len(seasons) >= 50, f"{sid}: only {len(seasons)} distinct seasons"
