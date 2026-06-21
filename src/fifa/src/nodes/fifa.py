"""FIFA/Coca-Cola World Ranking connector.

Publishes two long-format time-series subsets — the Men's and Women's national-team
World Ranking — one row per (release date, team).

Strategy (per research mechanism 'ranking_rest', host inside.fifa.com):
  1. GET https://inside.fifa.com/fifa-world-ranking/{men|women}, parse the embedded
     Next.js __NEXT_DATA__, read props.pageProps.pageData.ranking.allAvailableDates
     to get the full list of release dateIds [{id, date, matchWindowEndDate}].
  2. For each dateId, GET /api/ranking-overview?locale=en&dateId=<id> -> the full
     national-team table for that release.

Shape: stateless full re-pull. ~341 (men) + ~92 (women) small JSON requests per run;
overwriting each run picks up any historical revisions for free. The legacy
ranking-overview endpoint serves all historical 'idN' (men) / 'ranking_YYYYMMDD'
(women) dateIds; the ~6 newest releases per gender use a new 'FRS_*' dateId namespace
that the endpoint returns empty for, so those are skipped (the connector trails the
live site by ~one quarter — treated as not-yet-available, not an error).
"""

import json
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    save_raw_parquet,
    transient_retry,
)

PAGE_URL = {
    "fifa-men-world-ranking": "https://inside.fifa.com/fifa-world-ranking/men",
    "fifa-women-world-ranking": "https://inside.fifa.com/fifa-world-ranking/women",
}
GENDER = {
    "fifa-men-world-ranking": "men",
    "fifa-women-world-ranking": "women",
}

OVERVIEW_URL = "https://inside.fifa.com/api/ranking-overview"

SCHEMA = pa.schema([
    ("release_date", pa.string()),
    ("gender", pa.string()),
    ("rank", pa.int64()),
    ("id_team", pa.string()),
    ("team_name", pa.string()),
    ("country_code", pa.string()),
    ("total_points", pa.float64()),
    ("previous_rank", pa.int64()),
    ("previous_points", pa.float64()),
    ("confederation", pa.string()),
])


@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _get_overview(date_id: str) -> dict:
    resp = get(OVERVIEW_URL, params={"locale": "en", "dateId": date_id}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _release_dates(page_url: str) -> list[dict]:
    """Parse the page's __NEXT_DATA__ -> ranking.allAvailableDates (legacy ids only)."""
    html = _get_text(page_url)
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        raise AssertionError(f"no __NEXT_DATA__ in {page_url}")
    data = json.loads(m.group(1))
    ranking = data["props"]["pageProps"]["pageData"]["ranking"]
    dates = ranking.get("allAvailableDates") or []
    # FRS_* dateIds are not served by the legacy overview endpoint -> skip.
    return [d for d in dates if d.get("id") and not str(d["id"]).startswith("FRS")]


def fetch_ranking(node_id: str) -> None:
    asset = node_id
    gender = GENDER[node_id]
    configure_http(headers={"User-Agent": "subsets.io-connector/1.0 (+https://subsets.io)"})

    rows: list[dict] = []
    for entry in _release_dates(PAGE_URL[node_id]):
        date_id = entry["id"]
        release_date = entry.get("date") or entry.get("matchWindowEndDate")
        payload = _get_overview(date_id)
        rankings = payload.get("rankings") or []
        for r in rankings:
            item = r.get("rankingItem") or {}
            tag = r.get("tag") or {}
            rows.append({
                "release_date": release_date,
                "gender": gender,
                "rank": item.get("rank"),
                "id_team": item.get("idTeam"),
                "team_name": item.get("name"),
                "country_code": item.get("countryCode"),
                "total_points": item.get("totalPoints"),
                "previous_rank": item.get("previousRank"),
                "previous_points": r.get("previousPoints"),
                "confederation": tag.get("id"),
            })

    if not rows:
        raise AssertionError(f"{asset}: no ranking rows fetched")

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="fifa-men-world-ranking", fn=fetch_ranking, kind="download"),
    NodeSpec(id="fifa-women-world-ranking", fn=fetch_ranking, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(release_date AS DATE)   AS release_date,
                gender,
                CAST(rank AS INTEGER)        AS rank,
                id_team,
                team_name,
                country_code,
                CAST(total_points AS DOUBLE) AS total_points,
                CAST(previous_rank AS INTEGER) AS previous_rank,
                CAST(previous_points AS DOUBLE) AS previous_points,
                confederation
            FROM "{s.id}"
            WHERE release_date IS NOT NULL
              AND id_team IS NOT NULL
              AND rank IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY release_date, id_team ORDER BY rank
            ) = 1
        ''',
    )
    for s in DOWNLOAD_SPECS
]
