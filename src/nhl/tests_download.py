"""Health-invariant tests for the NHL connector raw assets.

Run post-DAG inside the connector; they load raw through subsets_utils, so they
behave identically locally and in the cloud.
"""

from subsets_utils import load_raw_ndjson

REFERENCE_IDS = {"nhl-season", "nhl-team", "nhl-franchise"}


def test_all_raw_assets_nonempty(spec_ids):
    """Every spec's raw NDJSON should hold rows. An empty payload usually means
    the endpoint switched format, the cayenneExp shape broke, or the host
    started 403/500-ing silently."""
    for sid in spec_ids:
        rows = load_raw_ndjson(sid)
        assert rows, f"{sid}: raw ndjson has 0 rows"


def test_reports_span_many_seasons(spec_ids):
    """Report assets are unions across 108 seasons. If pagination/season
    enumeration broke we'd see only the current season (or a single page)."""
    for sid in spec_ids:
        if sid in REFERENCE_IDS:
            continue
        rows = load_raw_ndjson(sid)
        seasons = {r.get("seasonId") for r in rows if r.get("seasonId") is not None}
        assert len(seasons) >= 20, (
            f"{sid}: only {len(seasons)} distinct seasons; expected many "
            f"(season enumeration or pagination likely degraded)"
        )


def test_reports_have_game_types(spec_ids):
    """Report rows are stamped with gameTypeId (2 regular / 3 playoffs)."""
    for sid in spec_ids:
        if sid in REFERENCE_IDS:
            continue
        rows = load_raw_ndjson(sid)
        gts = {r.get("gameTypeId") for r in rows}
        assert 2 in gts, f"{sid}: no regular-season (gameTypeId=2) rows; got {gts}"


def test_season_reference_complete(spec_ids):
    """The season catalog should list the full NHL history (~108 seasons)."""
    if "nhl-season" not in spec_ids:
        return
    rows = load_raw_ndjson("nhl-season")
    assert len(rows) >= 100, f"nhl-season: only {len(rows)} seasons; expected ~108"
