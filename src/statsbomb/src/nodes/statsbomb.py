"""StatsBomb open-data connector.

Source: https://github.com/statsbomb/open-data (raw.githubusercontent.com mirror).
Five publishable subsets, each its own schema:

  competitions  - one row per competition+season available in the repo (reference taxonomy).
  matches       - one row per match across all competition-seasons (flattened fixtures table).
  events        - long-format on-ball/off-ball event stream, unioned across all matches.
  lineups       - one row per player per match (roster / appearances).
  three_sixty   - exploded 360 freeze-frame player positions (selected matches only).

Fetch strategy (per research's chosen mechanism `github_raw_json`):
  competitions.json -> matches/{competition_id}/{season_id}.json -> per-match
  events/{match_id}.json, lineups/{match_id}.json, three-sixty/{match_id}.json.

competitions and matches are small enough for a stateless full re-pull written to a
single parquet asset. events / lineups / three_sixty span thousands of immutable
per-match files (~15M events total), so they are written as per-match parquet batches
(`statsbomb-<entity>-<match_id>.parquet`) with a resumable done-set watermark in state:
already-fetched matches are skipped, so the supervisor can interrupt and the next run
resumes without re-pulling. Matches are immutable once played, so closed batches never
change. Freshness (whether a node runs at all) is the maintain step's concern, not ours.
"""

import concurrent.futures as cf
import json

import httpx
import pyarrow as pa
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
)
from subsets_utils.retry import is_transient

RAW = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
# Per-match files are fetched concurrently — raw.githubusercontent.com has no
# documented rate limit and serves static files; ~12k tiny GETs would take hours
# sequentially. httpx.Client is thread-safe for concurrent requests.
CONCURRENCY = 24


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
def _retryable(exc: BaseException) -> bool:
    # Standard transient classification PLUS JSON decode errors: a truncated /
    # partially-read 200 body parses to a JSONDecodeError, which a re-fetch fixes
    # (observed on a large three-sixty file). JSONDecodeError subclasses ValueError.
    return is_transient(exc) or isinstance(exc, json.JSONDecodeError)


@retry(
    retry=retry_if_exception(_retryable),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _g(d, *path, default=None):
    """Safe nested getter: _g(e, 'type', 'name') -> e['type']['name'] or default."""
    cur = d
    for k in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur


def _coord(loc, idx):
    if isinstance(loc, list) and len(loc) > idx:
        v = loc[idx]
        return float(v) if isinstance(v, (int, float)) else None
    return None


def _competition_seasons():
    """All (competition_id, season_id) pairs from the root index."""
    return [(c["competition_id"], c["season_id"]) for c in _get_json(f"{RAW}/competitions.json")]


def _all_match_ids():
    """Every match_id across every competition-season, sorted and de-duplicated."""
    ids = set()
    for cid, sid in _competition_seasons():
        for m in _get_json(f"{RAW}/matches/{cid}/{sid}.json"):
            if m.get("match_id") is not None:
                ids.add(m["match_id"])
    return sorted(ids)


def _match_ids_with_360():
    ids = set()
    for cid, sid in _competition_seasons():
        for m in _get_json(f"{RAW}/matches/{cid}/{sid}.json"):
            if m.get("match_status_360") == "available" and m.get("match_id") is not None:
                ids.add(m["match_id"])
    return sorted(ids)


def _run_batched(node_id: str, match_ids, fetch_and_write):
    """Stateless full concurrent re-pull: write one raw batch parquet per match.

    Raw assets are run-scoped (each run writes into its own raw dir), so there is
    NO cross-run resumption to exploit — every run re-fetches the full corpus and
    re-writes all per-match batches. Concurrency (CONCURRENCY workers) keeps a full
    pull of thousands of small static files to a few minutes. Each worker writes a
    distinct asset id (`<node_id>-<match_id>`), so parallel writes never collide.
    Freshness (whether this node runs at all) is the maintain step's concern.

    A worker exception propagates and fails the node — except a permanent 4xx on a
    single match (a file flagged-available but absent), which is logged and skipped
    so one bad match can't sink the whole asset. Transient/JSON errors are already
    retried inside `_get_json`.
    """
    def _worker(mid):
        try:
            fetch_and_write(mid)
        except httpx.HTTPStatusError as exc:
            if exc.response is not None and 400 <= exc.response.status_code < 500:
                print(f"  [skip] {node_id} match {mid}: {exc.response.status_code} {exc.request.url}")
                return
            raise

    with cf.ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        for fut in cf.as_completed([ex.submit(_worker, m) for m in match_ids]):
            fut.result()  # re-raise any non-permanent failure -> node fails


# --------------------------------------------------------------------------- #
# competitions
# --------------------------------------------------------------------------- #
COMP_SCHEMA = pa.schema([
    ("competition_id", pa.int64()),
    ("season_id", pa.int64()),
    ("country_name", pa.string()),
    ("competition_name", pa.string()),
    ("competition_gender", pa.string()),
    ("competition_youth", pa.bool_()),
    ("competition_international", pa.bool_()),
    ("season_name", pa.string()),
    ("match_updated", pa.string()),
    ("match_updated_360", pa.string()),
    ("match_available", pa.string()),
    ("match_available_360", pa.string()),
])


def fetch_competitions(node_id: str) -> None:
    comps = _get_json(f"{RAW}/competitions.json")
    rows = [{
        "competition_id": c.get("competition_id"),
        "season_id": c.get("season_id"),
        "country_name": c.get("country_name"),
        "competition_name": c.get("competition_name"),
        "competition_gender": c.get("competition_gender"),
        "competition_youth": c.get("competition_youth"),
        "competition_international": c.get("competition_international"),
        "season_name": c.get("season_name"),
        "match_updated": c.get("match_updated"),
        "match_updated_360": c.get("match_updated_360"),
        "match_available": c.get("match_available"),
        "match_available_360": c.get("match_available_360"),
    } for c in comps]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=COMP_SCHEMA), node_id)


# --------------------------------------------------------------------------- #
# matches
# --------------------------------------------------------------------------- #
MATCH_SCHEMA = pa.schema([
    ("match_id", pa.int64()),
    ("match_date", pa.string()),
    ("kick_off", pa.string()),
    ("competition_id", pa.int64()),
    ("competition_name", pa.string()),
    ("country_name", pa.string()),
    ("season_id", pa.int64()),
    ("season_name", pa.string()),
    ("home_team_id", pa.int64()),
    ("home_team_name", pa.string()),
    ("away_team_id", pa.int64()),
    ("away_team_name", pa.string()),
    ("home_score", pa.int64()),
    ("away_score", pa.int64()),
    ("match_status", pa.string()),
    ("match_status_360", pa.string()),
    ("match_week", pa.int64()),
    ("competition_stage_id", pa.int64()),
    ("competition_stage_name", pa.string()),
    ("stadium_id", pa.int64()),
    ("stadium_name", pa.string()),
    ("referee_id", pa.int64()),
    ("referee_name", pa.string()),
    ("last_updated", pa.string()),
    ("last_updated_360", pa.string()),
])


def _match_row(m):
    return {
        "match_id": m.get("match_id"),
        "match_date": m.get("match_date"),
        "kick_off": m.get("kick_off"),
        "competition_id": _g(m, "competition", "competition_id"),
        "competition_name": _g(m, "competition", "competition_name"),
        "country_name": _g(m, "competition", "country_name"),
        "season_id": _g(m, "season", "season_id"),
        "season_name": _g(m, "season", "season_name"),
        "home_team_id": _g(m, "home_team", "home_team_id"),
        "home_team_name": _g(m, "home_team", "home_team_name"),
        "away_team_id": _g(m, "away_team", "away_team_id"),
        "away_team_name": _g(m, "away_team", "away_team_name"),
        "home_score": m.get("home_score"),
        "away_score": m.get("away_score"),
        "match_status": m.get("match_status"),
        "match_status_360": m.get("match_status_360"),
        "match_week": m.get("match_week"),
        "competition_stage_id": _g(m, "competition_stage", "id"),
        "competition_stage_name": _g(m, "competition_stage", "name"),
        "stadium_id": _g(m, "stadium", "id"),
        "stadium_name": _g(m, "stadium", "name"),
        "referee_id": _g(m, "referee", "id"),
        "referee_name": _g(m, "referee", "name"),
        "last_updated": m.get("last_updated"),
        "last_updated_360": m.get("last_updated_360"),
    }


def fetch_matches(node_id: str) -> None:
    rows = []
    for cid, sid in _competition_seasons():
        for m in _get_json(f"{RAW}/matches/{cid}/{sid}.json"):
            rows.append(_match_row(m))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=MATCH_SCHEMA), node_id)


# --------------------------------------------------------------------------- #
# events
# --------------------------------------------------------------------------- #
EVENT_SCHEMA = pa.schema([
    ("id", pa.string()),
    ("match_id", pa.int64()),
    ("index", pa.int64()),
    ("period", pa.int64()),
    ("timestamp", pa.string()),
    ("minute", pa.int64()),
    ("second", pa.int64()),
    ("duration", pa.float64()),
    ("type_id", pa.int64()),
    ("type_name", pa.string()),
    ("possession", pa.int64()),
    ("possession_team_id", pa.int64()),
    ("possession_team_name", pa.string()),
    ("play_pattern_id", pa.int64()),
    ("play_pattern_name", pa.string()),
    ("team_id", pa.int64()),
    ("team_name", pa.string()),
    ("player_id", pa.int64()),
    ("player_name", pa.string()),
    ("position_id", pa.int64()),
    ("position_name", pa.string()),
    ("location_x", pa.float64()),
    ("location_y", pa.float64()),
    ("under_pressure", pa.bool_()),
    ("counterpress", pa.bool_()),
    ("out", pa.bool_()),
    # pass
    ("pass_recipient_id", pa.int64()),
    ("pass_recipient_name", pa.string()),
    ("pass_length", pa.float64()),
    ("pass_angle", pa.float64()),
    ("pass_height_name", pa.string()),
    ("pass_end_x", pa.float64()),
    ("pass_end_y", pa.float64()),
    ("pass_body_part_name", pa.string()),
    ("pass_type_name", pa.string()),
    ("pass_outcome_name", pa.string()),
    # shot
    ("shot_statsbomb_xg", pa.float64()),
    ("shot_outcome_name", pa.string()),
    ("shot_type_name", pa.string()),
    ("shot_body_part_name", pa.string()),
    ("shot_technique_name", pa.string()),
    ("shot_end_x", pa.float64()),
    ("shot_end_y", pa.float64()),
])


def _event_row(e, match_id):
    loc = e.get("location")
    p_end = _g(e, "pass", "end_location")
    s_end = _g(e, "shot", "end_location")
    return {
        "id": e.get("id"),
        "match_id": match_id,
        "index": e.get("index"),
        "period": e.get("period"),
        "timestamp": e.get("timestamp"),
        "minute": e.get("minute"),
        "second": e.get("second"),
        "duration": e.get("duration"),
        "type_id": _g(e, "type", "id"),
        "type_name": _g(e, "type", "name"),
        "possession": e.get("possession"),
        "possession_team_id": _g(e, "possession_team", "id"),
        "possession_team_name": _g(e, "possession_team", "name"),
        "play_pattern_id": _g(e, "play_pattern", "id"),
        "play_pattern_name": _g(e, "play_pattern", "name"),
        "team_id": _g(e, "team", "id"),
        "team_name": _g(e, "team", "name"),
        "player_id": _g(e, "player", "id"),
        "player_name": _g(e, "player", "name"),
        "position_id": _g(e, "position", "id"),
        "position_name": _g(e, "position", "name"),
        "location_x": _coord(loc, 0),
        "location_y": _coord(loc, 1),
        "under_pressure": bool(e.get("under_pressure", False)),
        "counterpress": bool(e.get("counterpress", False)),
        "out": bool(e.get("out", False)),
        "pass_recipient_id": _g(e, "pass", "recipient", "id"),
        "pass_recipient_name": _g(e, "pass", "recipient", "name"),
        "pass_length": _g(e, "pass", "length"),
        "pass_angle": _g(e, "pass", "angle"),
        "pass_height_name": _g(e, "pass", "height", "name"),
        "pass_end_x": _coord(p_end, 0),
        "pass_end_y": _coord(p_end, 1),
        "pass_body_part_name": _g(e, "pass", "body_part", "name"),
        "pass_type_name": _g(e, "pass", "type", "name"),
        "pass_outcome_name": _g(e, "pass", "outcome", "name"),
        "shot_statsbomb_xg": _g(e, "shot", "statsbomb_xg"),
        "shot_outcome_name": _g(e, "shot", "outcome", "name"),
        "shot_type_name": _g(e, "shot", "type", "name"),
        "shot_body_part_name": _g(e, "shot", "body_part", "name"),
        "shot_technique_name": _g(e, "shot", "technique", "name"),
        "shot_end_x": _coord(s_end, 0),
        "shot_end_y": _coord(s_end, 1),
    }


def fetch_events(node_id: str) -> None:
    def _do(mid):
        events = _get_json(f"{RAW}/events/{mid}.json")
        rows = [_event_row(e, mid) for e in events]
        save_raw_parquet(pa.Table.from_pylist(rows, schema=EVENT_SCHEMA), f"{node_id}-{mid}")
        return True

    _run_batched(node_id, _all_match_ids(), _do)


# --------------------------------------------------------------------------- #
# lineups
# --------------------------------------------------------------------------- #
LINEUP_SCHEMA = pa.schema([
    ("match_id", pa.int64()),
    ("team_id", pa.int64()),
    ("team_name", pa.string()),
    ("player_id", pa.int64()),
    ("player_name", pa.string()),
    ("player_nickname", pa.string()),
    ("jersey_number", pa.int64()),
    ("country_id", pa.int64()),
    ("country_name", pa.string()),
    ("n_cards", pa.int64()),
    ("starting_position", pa.string()),
])


def _lineup_rows(teams, match_id):
    rows = []
    for t in teams:
        team_id = t.get("team_id")
        team_name = t.get("team_name")
        for p in t.get("lineup", []) or []:
            positions = p.get("positions") or []
            rows.append({
                "match_id": match_id,
                "team_id": team_id,
                "team_name": team_name,
                "player_id": p.get("player_id"),
                "player_name": p.get("player_name"),
                "player_nickname": p.get("player_nickname"),
                "jersey_number": p.get("jersey_number"),
                "country_id": _g(p, "country", "id"),
                "country_name": _g(p, "country", "name"),
                "n_cards": len(p.get("cards") or []),
                "starting_position": positions[0].get("position") if positions else None,
            })
    return rows


def fetch_lineups(node_id: str) -> None:
    def _do(mid):
        teams = _get_json(f"{RAW}/lineups/{mid}.json")
        save_raw_parquet(
            pa.Table.from_pylist(_lineup_rows(teams, mid), schema=LINEUP_SCHEMA),
            f"{node_id}-{mid}",
        )
        return True

    _run_batched(node_id, _all_match_ids(), _do)


# --------------------------------------------------------------------------- #
# three_sixty
# --------------------------------------------------------------------------- #
THREESIXTY_SCHEMA = pa.schema([
    ("event_uuid", pa.string()),
    ("match_id", pa.int64()),
    ("teammate", pa.bool_()),
    ("actor", pa.bool_()),
    ("keeper", pa.bool_()),
    ("x", pa.float64()),
    ("y", pa.float64()),
])


def _threesixty_rows(frames, match_id):
    rows = []
    for fr in frames:
        uuid = fr.get("event_uuid")
        for ff in fr.get("freeze_frame") or []:
            loc = ff.get("location")
            rows.append({
                "event_uuid": uuid,
                "match_id": match_id,
                "teammate": bool(ff.get("teammate", False)),
                "actor": bool(ff.get("actor", False)),
                "keeper": bool(ff.get("keeper", False)),
                "x": _coord(loc, 0),
                "y": _coord(loc, 1),
            })
    return rows


def fetch_three_sixty(node_id: str) -> None:
    def _do(mid):
        frames = _get_json(f"{RAW}/three-sixty/{mid}.json")
        save_raw_parquet(
            pa.Table.from_pylist(_threesixty_rows(frames, mid), schema=THREESIXTY_SCHEMA),
            f"{node_id}-{mid}",
        )
        return True

    _run_batched(node_id, _match_ids_with_360(), _do)


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="statsbomb-competitions", fn=fetch_competitions, kind="download"),
    NodeSpec(id="statsbomb-matches", fn=fetch_matches, kind="download"),
    NodeSpec(id="statsbomb-events", fn=fetch_events, kind="download"),
    NodeSpec(id="statsbomb-lineups", fn=fetch_lineups, kind="download"),
    NodeSpec(id="statsbomb-three-sixty", fn=fetch_three_sixty, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="statsbomb-competitions-transform",
        deps=["statsbomb-competitions"],
        sql='''
            SELECT
                CAST(competition_id AS BIGINT)            AS competition_id,
                CAST(season_id AS BIGINT)                 AS season_id,
                country_name,
                competition_name,
                competition_gender,
                CAST(competition_youth AS BOOLEAN)        AS competition_youth,
                CAST(competition_international AS BOOLEAN) AS competition_international,
                season_name,
                TRY_CAST(match_updated AS TIMESTAMP)      AS match_updated,
                TRY_CAST(match_updated_360 AS TIMESTAMP)  AS match_updated_360,
                TRY_CAST(match_available AS TIMESTAMP)    AS match_available,
                TRY_CAST(match_available_360 AS TIMESTAMP) AS match_available_360
            FROM "statsbomb-competitions"
            WHERE competition_id IS NOT NULL AND season_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="statsbomb-matches-transform",
        deps=["statsbomb-matches"],
        sql='''
            SELECT
                CAST(match_id AS BIGINT)              AS match_id,
                TRY_CAST(match_date AS DATE)          AS match_date,
                kick_off,
                competition_id,
                competition_name,
                country_name,
                season_id,
                season_name,
                home_team_id,
                home_team_name,
                away_team_id,
                away_team_name,
                home_score,
                away_score,
                match_status,
                match_status_360,
                match_week,
                competition_stage_id,
                competition_stage_name,
                stadium_id,
                stadium_name,
                referee_id,
                referee_name
            FROM "statsbomb-matches"
            WHERE match_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="statsbomb-events-transform",
        deps=["statsbomb-events"],
        sql='''
            SELECT *
            FROM "statsbomb-events"
            WHERE id IS NOT NULL AND match_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="statsbomb-lineups-transform",
        deps=["statsbomb-lineups"],
        sql='''
            SELECT *
            FROM "statsbomb-lineups"
            WHERE match_id IS NOT NULL AND player_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="statsbomb-three-sixty-transform",
        deps=["statsbomb-three-sixty"],
        sql='''
            SELECT *
            FROM "statsbomb-three-sixty"
            WHERE event_uuid IS NOT NULL AND match_id IS NOT NULL
        ''',
    ),
]
