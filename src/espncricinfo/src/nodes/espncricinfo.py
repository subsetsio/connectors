"""ESPNcricinfo connector.

Two data families, all stateless full re-pulls (overwrite each run):

1. REST (site.api.espn.com / site.web.api.espn.com) — cricket is organised as
   leagues (numeric ids). We crawl the *currently-active* leagues (from the
   personalized scoreboard header) plus a small pinned set of stable majors so
   the connector always has substantial data even off-season. Each league's
   scoreboard exposes a `calendar` of match dates; we fetch one scoreboard per
   calendar date to enumerate that league's events, then for scorecards we hit
   the per-event /summary endpoint.
     - matches          : one row per match (results, teams, venue, format)
     - batting_innings  : one row per batter per innings (from /summary rosters)
     - bowling_innings  : one row per bowler per innings (from /summary rosters)
   The scoreboard takes a single `dates=YYYYMMDD` (ranges return nothing), so the
   calendar-day crawl is the enumeration path. No incremental cursor — the active
   set is small and we re-pull it fully every run.

2. Statsguru (stats.espncricinfo.com) — server-rendered HTML aggregate-record
   tables. One generic fetch parses the records table for a `type`
   (batting/bowling/fielding/allround/team) across match classes 1/2/3
   (Test/ODI/T20I), paginating 50 rows/page until drained. Columns are slugified
   from the table headers; the match class becomes a column value.
"""

import re

import pyarrow as pa  # noqa: F401  (kept available; ndjson path used below)
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)

# --- config (data, not entity-union) ---------------------------------------
PINNED_LEAGUES = {"8048": "Indian Premier League"}  # stable major; guarantees data off-season
SG_CLASSES = {"1": "Test", "2": "ODI", "3": "T20I"}
SG_MAX_PAGES = 150          # safety ceiling per (class,type); raises if exceeded
MAX_DATES_PER_LEAGUE = 500  # safety ceiling on a league's calendar; raises if exceeded

SITE_API = "https://site.api.espn.com/apis"
WEB_API = "https://site.web.api.espn.com/apis"
SG_URL = "https://stats.espncricinfo.com/ci/engine/stats/index.html"


# --- HTTP helpers -----------------------------------------------------------
@transient_retry()
def _get_json(url, params=None):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_text(url, params=None):
    resp = get(url, params=params, timeout=(15.0, 120.0))
    resp.raise_for_status()
    return resp.text


# --- league / event crawl (shared by matches/batting/bowling) ---------------
def _active_leagues():
    """Active leagues from the personalized header, unioned with pinned majors.
    Returns list of (league_id, league_name)."""
    out = dict(PINNED_LEAGUES)
    data = _get_json(f"{SITE_API}/personalized/v2/scoreboard/header",
                     params={"sport": "cricket", "region": "in"})
    for sport in data.get("sports", []):
        for lg in sport.get("leagues", []):
            lid = str(lg.get("id"))
            if lid and lid != "None":
                out[lid] = lg.get("name") or out.get(lid) or lid
    return list(out.items())


def _league_calendar_dates(league_id):
    """YYYYMMDD strings for which this league has matches (from scoreboard calendar)."""
    sb = _get_json(f"{SITE_API}/site/v2/sports/cricket/{league_id}/scoreboard")
    leagues = sb.get("leagues") or []
    cal = leagues[0].get("calendar", []) if leagues else []
    dates = []
    seen = set()
    for entry in cal:
        # entries are ISO datetimes like "2026-03-28T00:00:00Z"
        d = str(entry)[:10].replace("-", "")
        if len(d) == 8 and d.isdigit() and d not in seen:
            seen.add(d)
            dates.append(d)
    if not dates:
        # off-season / single-event leagues: fall back to the default scoreboard
        dates = [None]
    if len(dates) > MAX_DATES_PER_LEAGUE:
        raise RuntimeError(
            f"league {league_id} calendar has {len(dates)} dates "
            f"(> {MAX_DATES_PER_LEAGUE}); refusing runaway crawl")
    return dates


def _collect_events():
    """List of (league_id, league_name, event) across active+pinned leagues."""
    events = []
    for league_id, league_name in _active_leagues():
        try:
            dates = _league_calendar_dates(league_id)
        except Exception as exc:  # noqa: BLE001 — one bad league must not kill the crawl
            print(f"[espncricinfo] league {league_id} calendar failed: "
                  f"{type(exc).__name__}: {exc}")
            continue
        seen_events = set()
        for d in dates:
            params = {"dates": d} if d else None
            try:
                sb = _get_json(
                    f"{SITE_API}/site/v2/sports/cricket/{league_id}/scoreboard",
                    params=params)
            except Exception as exc:  # noqa: BLE001
                print(f"[espncricinfo] scoreboard {league_id} {d} failed: "
                      f"{type(exc).__name__}: {exc}")
                continue
            for ev in sb.get("events", []):
                eid = str(ev.get("id"))
                if eid in seen_events:
                    continue
                seen_events.add(eid)
                events.append((league_id, league_name, ev))
    return events


def _match_row(league_id, league_name, ev):
    comps = ev.get("competitions") or []
    comp = comps[0] if comps else {}
    cls = comp.get("class") or {}
    venue = comp.get("venue") or {}
    addr = venue.get("address") or {}
    home = away = winner = home_score = away_score = None
    for c in comp.get("competitors", []):
        team = (c.get("team") or {}).get("displayName")
        if c.get("homeAway") == "home":
            home, home_score = team, c.get("score")
        elif c.get("homeAway") == "away":
            away, away_score = team, c.get("score")
        if str(c.get("winner")).lower() == "true":
            winner = team
    status = ((comp.get("status") or {}).get("type") or {}).get("description")
    season = ev.get("season")
    if isinstance(season, dict):
        season = season.get("year")
    return {
        "event_id": str(ev.get("id")),
        "league_id": str(league_id),
        "league_name": league_name,
        "format": cls.get("eventType"),
        "match_class": cls.get("generalClassCard") or cls.get("name"),
        "date": ev.get("date"),
        "season": season,
        "venue": venue.get("fullName"),
        "city": addr.get("city"),
        "country": addr.get("country"),
        "home_team": home,
        "away_team": away,
        "home_score": home_score,
        "away_score": away_score,
        "winner_team": winner,
        "status": status,
        "description": ev.get("description") or comp.get("description"),
    }


def _summary(league_id, event_id):
    return _get_json(f"{WEB_API}/site/v2/sports/cricket/{league_id}/summary",
                     params={"event": event_id})


def _flatten_period(period):
    """Merge all named stats in one innings/period entry into name->value."""
    out = {}
    for ls in period.get("linescores", []):
        stats = ls.get("statistics") or {}
        for cat in stats.get("categories", []):
            for s in cat.get("stats", []):
                out[s.get("name")] = s.get("value")
    return out


def _innings_lines(league_id, league_name, ev, summ, kind):
    """Yield batting or bowling rows from a /summary roster block."""
    event_id = str(ev.get("id"))
    rows = []
    for roster in summ.get("rosters", []):
        team = (roster.get("team") or {}).get("displayName")
        for player in roster.get("roster", []):
            ath = player.get("athlete") or {}
            pid = str(ath.get("id"))
            pname = ath.get("displayName")
            for per in player.get("linescores", []):
                d = _flatten_period(per)
                innings = d.get("inningsNumber") or per.get("period")
                if kind == "batting":
                    batted = (d.get("batted") or d.get("ballsFaced")
                              or d.get("runs") or d.get("dismissalCard"))
                    if "ballsFaced" not in d or not batted:
                        continue
                    rows.append({
                        "event_id": event_id,
                        "league_id": str(league_id),
                        "innings": innings,
                        "team": team,
                        "player_id": pid,
                        "player_name": pname,
                        "runs": d.get("runs"),
                        "balls": d.get("ballsFaced"),
                        "fours": d.get("fours"),
                        "sixes": d.get("sixes"),
                        "strike_rate": d.get("strikeRate"),
                        "batting_position": d.get("battingPosition"),
                        "not_out": d.get("notouts"),
                        "dismissal": d.get("dismissalCard"),
                    })
                else:  # bowling
                    bowled = (d.get("inningsBowled") or d.get("overs")
                              or d.get("balls") or d.get("wickets"))
                    if "overs" not in d or not bowled:
                        continue
                    rows.append({
                        "event_id": event_id,
                        "league_id": str(league_id),
                        "innings": innings,
                        "team": team,
                        "player_id": pid,
                        "player_name": pname,
                        "overs": d.get("overs"),
                        "maidens": d.get("maidens"),
                        "runs_conceded": d.get("conceded"),
                        "wickets": d.get("wickets"),
                        "economy": d.get("economyRate"),
                        "wides": d.get("wides"),
                        "noballs": d.get("noballs"),
                        "dots": d.get("dots"),
                        "bowling_position": d.get("bowlingPosition"),
                    })
    return rows


# --- fetch fns: REST --------------------------------------------------------
def fetch_matches(node_id: str) -> None:
    asset = node_id
    rows = [_match_row(lid, lname, ev) for lid, lname, ev in _collect_events()]
    save_raw_ndjson(rows, asset)


def fetch_batting_innings(node_id: str) -> None:
    _fetch_scorecards(node_id, "batting")


def fetch_bowling_innings(node_id: str) -> None:
    _fetch_scorecards(node_id, "bowling")


def _fetch_scorecards(node_id: str, kind: str) -> None:
    asset = node_id
    rows = []
    for league_id, league_name, ev in _collect_events():
        eid = str(ev.get("id"))
        try:
            summ = _summary(league_id, eid)
        except Exception as exc:  # noqa: BLE001 — skip an unreadable event, keep going
            print(f"[espncricinfo] summary {league_id}/{eid} failed: "
                  f"{type(exc).__name__}: {exc}")
            continue
        rows.extend(_innings_lines(league_id, league_name, ev, summ, kind))
    save_raw_ndjson(rows, asset)


# --- fetch fn: Statsguru ----------------------------------------------------
def _slug(header: str):
    h = header.strip().lower().replace("/", "_").replace("+", "plus").replace(" ", "_")
    h = re.sub(r"[^a-z0-9_]", "", h)
    if not h:
        return None
    if h[0].isdigit():
        h = "n" + h
    return h


def _parse_statsguru_page(text):
    """Return (headers, list-of-row-cell-lists) for the records data table."""
    tables = re.findall(r'<table[^>]*class="engineTable"[^>]*>.*?</table>', text, re.S)
    for t in tables:
        data_rows = re.findall(r'<tr[^>]*class="data1"[^>]*>(.*?)</tr>', t, re.S)
        if len(data_rows) < 3:
            continue
        ths = re.findall(r"<th[^>]*>(.*?)</th>", t, re.S)
        headers = [re.sub("<.*?>", "", h) for h in ths]
        headers = [h.replace("&nbsp;", " ").strip() for h in headers]
        parsed = []
        for r in data_rows:
            tds = re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)
            cells = [re.sub("<.*?>", "", c).replace("&nbsp;", " ").strip() for c in tds]
            parsed.append(cells)
        return headers, parsed
    return None, []


def fetch_statsguru(node_id: str) -> None:
    asset = node_id
    typ = node_id.rsplit("-", 1)[-1]  # e.g. espncricinfo-statsguru-batting -> batting
    rows = []
    for cls, cls_name in SG_CLASSES.items():
        page = 1
        keys = None
        while True:
            if page > SG_MAX_PAGES:
                raise RuntimeError(
                    f"statsguru {typ} class={cls} exceeded {SG_MAX_PAGES} pages; "
                    f"refusing runaway crawl")
            text = _get_text(SG_URL, params={
                "class": cls, "template": "results", "type": typ, "page": page})
            headers, parsed = _parse_statsguru_page(text)
            if not parsed:
                break
            if keys is None:
                keys = [_slug(h) for h in headers]
            for cells in parsed:
                row = {"match_class": cls_name}
                for k, v in zip(keys, cells):
                    if k:
                        row[k] = v if v not in ("", "-") else None
                rows.append(row)
            if len(parsed) < 50:
                break
            page += 1
    save_raw_ndjson(rows, asset)


# --- DOWNLOAD_SPECS ---------------------------------------------------------
DOWNLOAD_SPECS = [
    NodeSpec(id="espncricinfo-matches", fn=fetch_matches, kind="download"),
    NodeSpec(id="espncricinfo-batting-innings", fn=fetch_batting_innings, kind="download"),
    NodeSpec(id="espncricinfo-bowling-innings", fn=fetch_bowling_innings, kind="download"),
    NodeSpec(id="espncricinfo-statsguru-batting", fn=fetch_statsguru, kind="download"),
    NodeSpec(id="espncricinfo-statsguru-bowling", fn=fetch_statsguru, kind="download"),
    NodeSpec(id="espncricinfo-statsguru-fielding", fn=fetch_statsguru, kind="download"),
    NodeSpec(id="espncricinfo-statsguru-allround", fn=fetch_statsguru, kind="download"),
    NodeSpec(id="espncricinfo-statsguru-team", fn=fetch_statsguru, kind="download"),
]


# --- TRANSFORM_SPECS --------------------------------------------------------
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="espncricinfo-matches-transform",
        deps=["espncricinfo-matches"],
        sql='''
            SELECT
                CAST(event_id AS BIGINT)            AS event_id,
                CAST(league_id AS BIGINT)           AS league_id,
                league_name,
                format,
                match_class,
                -- ESPN stamps "YYYY-MM-DDTHH:MMZ" (and occasionally with seconds);
                -- neither parses via a plain TIMESTAMP cast, so try both formats.
                coalesce(
                    try_strptime(date, '%Y-%m-%dT%H:%MZ'),
                    try_strptime(date, '%Y-%m-%dT%H:%M:%SZ')
                )                                   AS start_time,
                CAST(substr(date, 1, 10) AS DATE)   AS match_date,
                TRY_CAST(season AS INTEGER)         AS season,
                venue, city, country,
                home_team, away_team,
                home_score, away_score, winner_team,
                status, description
            FROM "espncricinfo-matches"
            WHERE event_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="espncricinfo-batting-innings-transform",
        deps=["espncricinfo-batting-innings"],
        sql='''
            SELECT
                CAST(event_id AS BIGINT)      AS event_id,
                CAST(league_id AS BIGINT)     AS league_id,
                TRY_CAST(innings AS INTEGER)  AS innings,
                team,
                CAST(player_id AS BIGINT)     AS player_id,
                player_name,
                TRY_CAST(runs AS INTEGER)     AS runs,
                TRY_CAST(balls AS INTEGER)    AS balls,
                TRY_CAST(fours AS INTEGER)    AS fours,
                TRY_CAST(sixes AS INTEGER)    AS sixes,
                TRY_CAST(strike_rate AS DOUBLE) AS strike_rate,
                TRY_CAST(batting_position AS INTEGER) AS batting_position,
                TRY_CAST(not_out AS INTEGER)  AS not_out,
                dismissal
            FROM "espncricinfo-batting-innings"
            WHERE player_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="espncricinfo-bowling-innings-transform",
        deps=["espncricinfo-bowling-innings"],
        sql='''
            SELECT
                CAST(event_id AS BIGINT)      AS event_id,
                CAST(league_id AS BIGINT)     AS league_id,
                TRY_CAST(innings AS INTEGER)  AS innings,
                team,
                CAST(player_id AS BIGINT)     AS player_id,
                player_name,
                TRY_CAST(overs AS DOUBLE)     AS overs,
                TRY_CAST(maidens AS INTEGER)  AS maidens,
                TRY_CAST(runs_conceded AS INTEGER) AS runs_conceded,
                TRY_CAST(wickets AS INTEGER)  AS wickets,
                TRY_CAST(economy AS DOUBLE)   AS economy,
                TRY_CAST(wides AS INTEGER)    AS wides,
                TRY_CAST(noballs AS INTEGER)  AS noballs,
                TRY_CAST(dots AS INTEGER)     AS dots,
                TRY_CAST(bowling_position AS INTEGER) AS bowling_position
            FROM "espncricinfo-bowling-innings"
            WHERE player_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="espncricinfo-statsguru-batting-transform",
        deps=["espncricinfo-statsguru-batting"],
        sql='''
            SELECT
                match_class,
                trim(regexp_replace(player, '\\(.*\\)', '')) AS player,
                regexp_extract(player, '\\(([^)]+)\\)', 1)   AS country,
                span,
                TRY_CAST(mat AS INTEGER)  AS matches,
                TRY_CAST(inns AS INTEGER) AS innings,
                TRY_CAST(no AS INTEGER)   AS not_outs,
                TRY_CAST(runs AS INTEGER) AS runs,
                hs                        AS highest_score,
                TRY_CAST(ave AS DOUBLE)   AS average,
                TRY_CAST(n100 AS INTEGER) AS hundreds,
                TRY_CAST(n50 AS INTEGER)  AS fifties,
                TRY_CAST(n0 AS INTEGER)   AS ducks
            FROM "espncricinfo-statsguru-batting"
            WHERE player IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="espncricinfo-statsguru-bowling-transform",
        deps=["espncricinfo-statsguru-bowling"],
        sql='''
            SELECT
                match_class,
                trim(regexp_replace(player, '\\(.*\\)', '')) AS player,
                regexp_extract(player, '\\(([^)]+)\\)', 1)   AS country,
                span,
                TRY_CAST(mat AS INTEGER)   AS matches,
                TRY_CAST(inns AS INTEGER)  AS innings,
                TRY_CAST(balls AS INTEGER) AS balls,
                TRY_CAST(runs AS INTEGER)  AS runs_conceded,
                TRY_CAST(wkts AS INTEGER)  AS wickets,
                bbi                        AS best_innings,
                bbm                        AS best_match,
                TRY_CAST(ave AS DOUBLE)    AS average,
                TRY_CAST(econ AS DOUBLE)   AS economy,
                TRY_CAST(sr AS DOUBLE)     AS strike_rate,
                TRY_CAST(n5 AS INTEGER)    AS five_wkts,
                TRY_CAST(n10 AS INTEGER)   AS ten_wkts
            FROM "espncricinfo-statsguru-bowling"
            WHERE player IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="espncricinfo-statsguru-fielding-transform",
        deps=["espncricinfo-statsguru-fielding"],
        sql='''
            SELECT
                match_class,
                trim(regexp_replace(player, '\\(.*\\)', '')) AS player,
                regexp_extract(player, '\\(([^)]+)\\)', 1)   AS country,
                span,
                TRY_CAST(mat AS INTEGER)  AS matches,
                TRY_CAST(inns AS INTEGER) AS innings,
                TRY_CAST(dis AS INTEGER)  AS dismissals,
                TRY_CAST(ct AS INTEGER)   AS caught,
                TRY_CAST(st AS INTEGER)   AS stumped,
                TRY_CAST(ct_wk AS INTEGER) AS caught_keeper,
                TRY_CAST(ct_fi AS INTEGER) AS caught_fielder,
                TRY_CAST(md AS INTEGER)   AS max_dismissals_innings,
                TRY_CAST(d_i AS DOUBLE)   AS dismissals_per_innings
            FROM "espncricinfo-statsguru-fielding"
            WHERE player IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="espncricinfo-statsguru-allround-transform",
        deps=["espncricinfo-statsguru-allround"],
        sql='''
            SELECT
                match_class,
                trim(regexp_replace(player, '\\(.*\\)', '')) AS player,
                regexp_extract(player, '\\(([^)]+)\\)', 1)   AS country,
                span,
                TRY_CAST(mat AS INTEGER)    AS matches,
                TRY_CAST(runs AS INTEGER)   AS runs,
                hs                          AS highest_score,
                TRY_CAST(bat_av AS DOUBLE)  AS batting_average,
                TRY_CAST(n100 AS INTEGER)   AS hundreds,
                TRY_CAST(wkts AS INTEGER)   AS wickets,
                bbi                         AS best_innings,
                TRY_CAST(bowl_av AS DOUBLE) AS bowling_average,
                TRY_CAST(n5 AS INTEGER)     AS five_wkts,
                TRY_CAST(ct AS INTEGER)     AS catches,
                TRY_CAST(st AS INTEGER)     AS stumpings,
                TRY_CAST(ave_diff AS DOUBLE) AS average_difference
            FROM "espncricinfo-statsguru-allround"
            WHERE player IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="espncricinfo-statsguru-team-transform",
        deps=["espncricinfo-statsguru-team"],
        sql='''
            SELECT
                match_class,
                team,
                span,
                TRY_CAST(mat AS INTEGER)  AS matches,
                TRY_CAST(won AS INTEGER)  AS won,
                TRY_CAST(lost AS INTEGER) AS lost,
                TRY_CAST(tied AS INTEGER) AS tied,
                TRY_CAST(draw AS INTEGER) AS drawn,
                TRY_CAST(w_l AS DOUBLE)   AS win_loss_ratio,
                TRY_CAST(ave AS DOUBLE)   AS average,
                TRY_CAST(rpo AS DOUBLE)   AS runs_per_over,
                TRY_CAST(inns AS INTEGER) AS innings,
                hs                        AS highest_score,
                ls                        AS lowest_score
            FROM "espncricinfo-statsguru-team"
            WHERE team IS NOT NULL
        ''',
    ),
]
