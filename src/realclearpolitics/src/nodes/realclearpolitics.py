"""RealClearPolitics poll-average connector.

Mechanism (from research): the per-race JSON endpoint
``https://orig.realclearpolitics.com/poll/race/<id>/polling_data.json`` on the
un-walled ``orig`` subdomain (www / realclearpolling.com sit behind a DataDome
bot wall). Race ids are enumerated from the static ``latest_polls`` index pages
on the same host.

Two published subsets, both derived from the same race corpus:
  * ``poll_readings`` — long-format poll readings (one row per race x poll x
    candidate), including the RCP-average rows.
  * ``races`` — reference catalog (one row per race).

Shape: stateless full re-pull. The active corpus is ~100 races x ~28KB, fetched
in full every run and overwritten downstream. No watermark / cursor — revisions
to historical averages are picked up for free.
"""

import re

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)
import httpx

BASE = "https://orig.realclearpolitics.com"

INDEX_PAGES = [
    "/epolls/latest_polls/",
    "/epolls/latest_polls/elections/",
    "/epolls/latest_polls/senate/",
    "/epolls/latest_polls/governor/",
    "/epolls/latest_polls/house/",
    "/epolls/latest_polls/dem_primaries/",
    "/epolls/latest_polls/gop_primaries/",
    "/epolls/latest_polls/state_of_the_union/",
]

_RACE_HREF = re.compile(r'href="([^"]*?-(\d+)\.html)"')


@transient_retry()
def _get_text(url):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _get_json(url):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _enumerate_races():
    """Union of (race_id, href) across the latest_polls index pages."""
    races = {}
    for page in INDEX_PAGES:
        html = _get_text(BASE + page)
        for href, rid in _RACE_HREF.findall(html):
            if "/epolls/" in href:
                races[rid] = href
    return races


def _classify(href):
    """(year, office) derived from an epolls href path."""
    m = re.search(r"/epolls/(\d{4})/", href)
    year = m.group(1) if m else None
    office = "other"
    for o in ("president", "senate", "governor", "house"):
        if "/{}/".format(o) in href:
            office = o
            break
    if "/epolls/other/" in href:
        office = "other"
    return year, office


def _race_json(race_id):
    """Fetch one race's polling_data.json. Returns the parsed dict, or None on a
    permanent 4xx (race listed on the index but no JSON behind it)."""
    url = "{}/poll/race/{}/polling_data.json".format(BASE, race_id)
    try:
        return _get_json(url)
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        if status != 429 and 400 <= status < 500:
            print("skip race {}: permanent HTTP {}".format(race_id, status))
            return None
        raise


def _candidate_names(poll_rows):
    for row in poll_rows:
        cands = row.get("candidate") or []
        names = [c.get("name") for c in cands if c.get("name")]
        if names:
            return names
    return []


def fetch_poll_readings(node_id: str) -> None:
    """Long-format poll readings across all enumerated races."""
    asset = node_id
    races = _enumerate_races()
    rows = []
    for rid, href in races.items():
        data = _race_json(rid)
        if not data:
            continue
        mi = data.get("moduleInfo", {}) or {}
        year, office = _classify(href)
        race_title = mi.get("title")
        state = mi.get("state")
        country = mi.get("country")
        category = mi.get("category")
        last_build = mi.get("lastBuildDate")
        for poll in data.get("poll", []) or []:
            ptype = poll.get("type")
            reading_type = "rcp_average" if ptype == "rcp_average" else "poll"
            spread = poll.get("spread") or {}
            for cand in poll.get("candidate") or []:
                rows.append({
                    "race_id": int(rid),
                    "race_title": race_title,
                    "office": office,
                    "year": year,
                    "state": state,
                    "country": country,
                    "category": category,
                    "reading_type": reading_type,
                    "poll_id": poll.get("id"),
                    "pollster": poll.get("pollster"),
                    "date_label": poll.get("date"),
                    "data_start_date": poll.get("data_start_date") or None,
                    "data_end_date": poll.get("data_end_date") or None,
                    "sample_size_raw": poll.get("sampleSize") or None,
                    "margin_error": poll.get("marginError") or None,
                    "partisan": poll.get("partisan") or None,
                    "candidate": cand.get("name"),
                    "affiliation": cand.get("affiliation") or None,
                    "value": cand.get("value") or None,
                    "spread_candidate": spread.get("name") or None,
                    "spread_value": spread.get("value") or None,
                    "last_build_date": last_build,
                })
    if not rows:
        raise RuntimeError("no poll readings produced — enumeration or fetch broke")
    save_raw_ndjson(rows, asset)


def fetch_races(node_id: str) -> None:
    """Reference catalog: one row per enumerated race."""
    asset = node_id
    races = _enumerate_races()
    rows = []
    for rid, href in races.items():
        data = _race_json(rid)
        if not data:
            continue
        mi = data.get("moduleInfo", {}) or {}
        poll_rows = data.get("poll", []) or []
        year, office = _classify(href)
        names = _candidate_names(poll_rows)
        num_polls = sum(1 for p in poll_rows if p.get("type") != "rcp_average")
        rows.append({
            "race_id": int(rid),
            "title": mi.get("title"),
            "office": office,
            "year": year,
            "state": mi.get("state") or None,
            "country": mi.get("country") or None,
            "category": mi.get("category") or None,
            "slug": mi.get("poll_contentful_slug") or None,
            "fullpath": mi.get("poll_contentful_fullpath") or None,
            "link": mi.get("link") or None,
            "num_candidates": len(names),
            "candidate_names": ", ".join(names) if names else None,
            "num_polls": num_polls,
            "last_build_date": mi.get("lastBuildDate"),
        })
    if not rows:
        raise RuntimeError("no races produced — enumeration or fetch broke")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="realclearpolitics-poll-readings", fn=fetch_poll_readings, kind="download"),
    NodeSpec(id="realclearpolitics-races", fn=fetch_races, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="realclearpolitics-poll-readings-transform",
        deps=["realclearpolitics-poll-readings"],
        sql='''
            SELECT
                CAST(race_id AS BIGINT)                         AS race_id,
                CAST(race_title AS VARCHAR)                     AS race_title,
                CAST(office AS VARCHAR)                         AS office,
                TRY_CAST(year AS INTEGER)                       AS year,
                CAST(state AS VARCHAR)                          AS state,
                CAST(country AS VARCHAR)                        AS country,
                CAST(category AS VARCHAR)                       AS category,
                CAST(reading_type AS VARCHAR)                   AS reading_type,
                CAST(poll_id AS VARCHAR)                        AS poll_id,
                CAST(pollster AS VARCHAR)                       AS pollster,
                CAST(date_label AS VARCHAR)                     AS date_label,
                TRY_CAST(strptime(CAST(data_start_date AS VARCHAR), '%Y/%m/%d') AS DATE) AS poll_start_date,
                TRY_CAST(strptime(CAST(data_end_date   AS VARCHAR), '%Y/%m/%d') AS DATE) AS poll_end_date,
                TRY_CAST(regexp_extract(CAST(sample_size_raw AS VARCHAR), '[0-9]+') AS INTEGER) AS sample_size,
                NULLIF(regexp_extract(CAST(sample_size_raw AS VARCHAR), '[A-Za-z]+$'), '')      AS sample_population,
                TRY_CAST(margin_error AS DOUBLE)                AS margin_error,
                NULLIF(CAST(partisan AS VARCHAR), '')           AS partisan,
                CAST(candidate AS VARCHAR)                      AS candidate,
                CAST(affiliation AS VARCHAR)                    AS affiliation,
                TRY_CAST(value AS DOUBLE)                       AS value,
                CAST(spread_candidate AS VARCHAR)               AS spread_candidate,
                CAST(spread_value AS VARCHAR)                   AS spread_value,
                CAST(last_build_date AS VARCHAR)                AS last_build_date
            FROM "realclearpolitics-poll-readings"
            WHERE candidate IS NOT NULL
              AND TRY_CAST(value AS DOUBLE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="realclearpolitics-races-transform",
        deps=["realclearpolitics-races"],
        sql='''
            SELECT
                CAST(race_id AS BIGINT)         AS race_id,
                CAST(title AS VARCHAR)          AS title,
                CAST(office AS VARCHAR)         AS office,
                TRY_CAST(year AS INTEGER)       AS year,
                CAST(state AS VARCHAR)          AS state,
                CAST(country AS VARCHAR)        AS country,
                CAST(category AS VARCHAR)       AS category,
                CAST(slug AS VARCHAR)           AS slug,
                CAST(fullpath AS VARCHAR)       AS fullpath,
                CAST(link AS VARCHAR)           AS link,
                CAST(num_candidates AS INTEGER) AS num_candidates,
                CAST(candidate_names AS VARCHAR) AS candidate_names,
                CAST(num_polls AS INTEGER)      AS num_polls,
                CAST(last_build_date AS VARCHAR) AS last_build_date
            FROM "realclearpolitics-races"
            WHERE race_id IS NOT NULL
        ''',
    ),
]
