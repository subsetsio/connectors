"""TwitchTracker connector — Twitch channel & game/category statistics.

Source: https://twitchtracker.com/api (third-party Twitch analytics aggregator).

Two per-entity JSON endpoints, both trailing-30-day rolling SUMMARIES that
return a single flat object per entity (NOT a time series):

  GET /channels/summary/{login}      -> {rank, minutes_streamed, avg_viewers,
                                          max_viewers, hours_watched, followers,
                                          followers_total}
  GET /games/summary/{id_or_name}    -> {avg_viewers, avg_channels, rank,
                                          hours_watched}

Shape: snapshot-only full re-pull (decision shape (1)/(e)). There is no list
endpoint and no incremental filter, so each refresh re-fetches the current
30-day summary for every seeded entity and overwrites the previous snapshot.
The seed lists (which channels / games to query) are curated data in
src/constants.py — the API cannot enumerate them and scraping is prohibited.

Untracked / inactive entities return an empty object `{}` with HTTP 200; those
rows are skipped. The site enforces an undocumented burst rate limit (observed
~14 rapid requests then HTTP 429 with an HTML body), so requests are throttled
per process and 429/5xx/transport errors are retried with backoff.
"""

import logging
from datetime import datetime, timezone
from urllib.parse import quote

import pyarrow as pa
from ratelimit import limits, sleep_and_retry

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import CHANNEL_LOGINS, GAMES

log = logging.getLogger("twitch-tracker")

BASE = "https://twitchtracker.com/api"

# Per-process throttle. The host has an undocumented burst limit; ~12 calls/min
# per process keeps well under it (two sibling specs run in separate processes,
# so combined load is ~24/min) and transient_retry rides out any 429 spikes.
_RL_CALLS = 12
_RL_PERIOD = 60

CHANNELS_SCHEMA = pa.schema([
    ("channel", pa.string()),
    ("rank", pa.int64()),
    ("minutes_streamed", pa.int64()),
    ("avg_viewers", pa.int64()),
    ("max_viewers", pa.int64()),
    ("hours_watched", pa.int64()),
    ("followers", pa.int64()),          # net 30-day change; may be negative
    ("followers_total", pa.int64()),
    ("captured_date", pa.date32()),
])

GAMES_SCHEMA = pa.schema([
    ("game", pa.string()),
    ("rank", pa.int64()),
    ("avg_viewers", pa.int64()),
    ("avg_channels", pa.int64()),
    ("hours_watched", pa.int64()),
    ("captured_date", pa.date32()),
])


@sleep_and_retry
@limits(calls=_RL_CALLS, period=_RL_PERIOD)
@transient_retry(attempts=8, min_wait=2, max_wait=120)
def _fetch_summary(url: str) -> dict:
    """GET a summary endpoint and return the parsed JSON object.

    raise_for_status() runs inside the retry so 429 (rate limit, HTML body) and
    5xx are classified transient and retried. A 200 with an empty `{}` body
    (entity not tracked / no activity in the window) returns {} for the caller
    to skip.
    """
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def fetch_channels(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    captured = datetime.now(timezone.utc).date()
    rows = []
    skipped = 0
    for login in CHANNEL_LOGINS:
        data = _fetch_summary(f"{BASE}/channels/summary/{quote(login)}")
        if not data:  # empty object => not tracked / no activity in the window
            skipped += 1
            log.info("twitch-tracker channels: no data for %r, skipping", login)
            continue
        rows.append({
            "channel": login,
            "rank": data.get("rank"),
            "minutes_streamed": data.get("minutes_streamed"),
            "avg_viewers": data.get("avg_viewers"),
            "max_viewers": data.get("max_viewers"),
            "hours_watched": data.get("hours_watched"),
            "followers": data.get("followers"),
            "followers_total": data.get("followers_total"),
            "captured_date": captured,
        })
    if not rows:
        # Every seeded channel returned empty: the endpoint shape almost
        # certainly changed (or we are wholly rate-limited). Fail loudly rather
        # than publish an empty snapshot.
        raise RuntimeError(
            f"twitch-tracker channels: 0 rows from {len(CHANNEL_LOGINS)} seeds "
            "— endpoint shape changed or fully rate-limited?"
        )
    log.info("twitch-tracker channels: %d rows, %d skipped", len(rows), skipped)
    table = pa.Table.from_pylist(rows, schema=CHANNELS_SCHEMA)
    save_raw_parquet(table, asset)


def fetch_games(node_id: str) -> None:
    asset = node_id
    captured = datetime.now(timezone.utc).date()
    rows = []
    skipped = 0
    for game in GAMES:
        data = _fetch_summary(f"{BASE}/games/summary/{quote(game)}")
        if not data:
            skipped += 1
            log.info("twitch-tracker games: no data for %r, skipping", game)
            continue
        rows.append({
            "game": game,
            "rank": data.get("rank"),
            "avg_viewers": data.get("avg_viewers"),
            "avg_channels": data.get("avg_channels"),
            "hours_watched": data.get("hours_watched"),
            "captured_date": captured,
        })
    if not rows:
        raise RuntimeError(
            f"twitch-tracker games: 0 rows from {len(GAMES)} seeds "
            "— endpoint shape changed or fully rate-limited?"
        )
    log.info("twitch-tracker games: %d rows, %d skipped", len(rows), skipped)
    table = pa.Table.from_pylist(rows, schema=GAMES_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="twitch-tracker-channels", fn=fetch_channels, kind="download"),
    NodeSpec(id="twitch-tracker-games", fn=fetch_games, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="twitch-tracker-channels-transform",
        deps=["twitch-tracker-channels"],
        sql='''
            SELECT
                channel,
                CAST(rank AS INTEGER)             AS rank,
                CAST(minutes_streamed AS BIGINT)  AS minutes_streamed,
                CAST(avg_viewers AS BIGINT)       AS avg_viewers,
                CAST(max_viewers AS BIGINT)       AS max_viewers,
                CAST(hours_watched AS BIGINT)     AS hours_watched,
                CAST(followers AS BIGINT)         AS followers,
                CAST(followers_total AS BIGINT)   AS followers_total,
                CAST(captured_date AS DATE)       AS captured_date
            FROM "twitch-tracker-channels"
            WHERE channel IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="twitch-tracker-games-transform",
        deps=["twitch-tracker-games"],
        sql='''
            SELECT
                game,
                CAST(rank AS INTEGER)         AS rank,
                CAST(avg_viewers AS BIGINT)   AS avg_viewers,
                CAST(avg_channels AS BIGINT)  AS avg_channels,
                CAST(hours_watched AS BIGINT) AS hours_watched,
                CAST(captured_date AS DATE)   AS captured_date
            FROM "twitch-tracker-games"
            WHERE game IS NOT NULL
        ''',
    ),
]
