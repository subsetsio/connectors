"""IOC (olympics.com) connector — Olympic medal table by NOC.

Source & mechanism (see research `odf_json`): the IOC publishes its results as
static JSON files (the web materialisation of the Olympic Data Feed) on the
olympics.com Akamai CDN, e.g.
  https://olympics.com/<COMP>/data/CIS_MedalNOCs~lang=ENG~comp=<COMP>.json
Confirmed editions exposing this feed: OG2024 (Paris 2024 Olympic Games) and
PG2024 (Paris 2024 Paralympic Games). Older editions do not expose it.

CIS_MedalNOCs payload (verified): {"medalNOC":[{gender, sport, gold, silver,
bronze, total, rank, rankEqual, sortRank, rankTotal, rankTotalEqual,
sortRankTotal, org, organisation:{code, description, longDescription, ...}}]}.
One row per NOC x sport x gender. sport='GLO' is the all-sports aggregate;
gender='TOT' is the all-genders aggregate; gender values M/W/X/O are
men/women/mixed/open.

ACCESS REALITY: olympics.com sits behind Akamai bot management that resets the
connection for automated / datacenter-IP clients — every direct probe (curl,
headless Chromium, httpx) was refused. The 2024 Games are concluded, so these
files are frozen. The robust, verified-reachable source is therefore the
Wayback Machine: enumerate the latest archived snapshot via the CDX API and
fetch the raw (gzip-encoded) body via the `id_` endpoint. We still TRY the live
origin first (a cloud runner with a clean IP may reach it and it is the
authoritative copy); on any failure or a non-JSON bot-challenge response we
fall back to Wayback. Stateless full re-pull: both editions are re-fetched and
overwritten every run; no watermark (the data is immutable).
"""
import gzip
import json

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

# Confirmed Games editions that publish the CIS_MedalNOCs feed.
EDITIONS = [
    ("OG2024", "Olympic"),
    ("PG2024", "Paralympic"),
]

_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

SCHEMA = pa.schema([
    ("edition", pa.string()),
    ("games", pa.string()),
    ("noc_code", pa.string()),
    ("noc_name", pa.string()),
    ("sport", pa.string()),
    ("gender", pa.string()),
    ("gold", pa.int64()),
    ("silver", pa.int64()),
    ("bronze", pa.int64()),
    ("total", pa.int64()),
    ("rank", pa.int64()),
    ("rank_total", pa.int64()),
])


@transient_retry()
def _get_json(url: str, **kwargs):
    resp = get(url, timeout=(10.0, 120.0), **kwargs)
    resp.raise_for_status()
    body = resp.content
    # Wayback `id_` serves the original (often gzip-encoded) bytes verbatim.
    try:
        body = gzip.decompress(body)
    except (OSError, gzip.BadGzipFile):
        pass
    return json.loads(body)


def _live_url(comp: str) -> str:
    return f"https://olympics.com/{comp}/data/CIS_MedalNOCs~lang=ENG~comp={comp}.json"


def _wayback_latest(comp: str) -> dict:
    """Newest archived CIS_MedalNOCs (ENG) snapshot for `comp`, via CDX + id_."""
    resp = get(
        "https://web.archive.org/cdx/search/cdx",
        params={
            "url": f"olympics.com/{comp}/data/CIS_MedalNOCs",
            "matchType": "prefix",
            "output": "json",
            "fl": "timestamp,original",
            "filter": "statuscode:200",
        },
        timeout=(10.0, 60.0),
    )
    resp.raise_for_status()
    rows = resp.json()[1:]  # drop header row
    cands = [
        (ts, orig)
        for ts, orig in rows
        if "lang=ENG" in orig and f"comp={comp}" in orig
    ]
    if not cands:
        raise RuntimeError(f"no archived CIS_MedalNOCs ENG snapshot for {comp}")
    ts, orig = max(cands, key=lambda x: x[0])  # latest = final frozen table
    return _get_json(f"https://web.archive.org/web/{ts}id_/{orig}")


def _try_live(comp: str) -> dict | None:
    """Single fast attempt at the bot-protected live origin (no retry storm).

    olympics.com resets the connection for datacenter IPs, so we do NOT retry
    here — one short attempt, then fall back to Wayback. A cloud runner with a
    clean IP that DOES reach the origin still benefits."""
    resp = get(_live_url(comp), headers=_BROWSER_HEADERS, timeout=(5.0, 20.0))
    resp.raise_for_status()
    body = resp.content
    try:
        body = gzip.decompress(body)
    except (OSError, gzip.BadGzipFile):
        pass
    return json.loads(body)


def _fetch_medal_payload(comp: str) -> dict:
    """Live origin first (authoritative); Wayback fallback (verified reachable)."""
    try:
        payload = _try_live(comp)
        if isinstance(payload, dict) and isinstance(payload.get("medalNOC"), list):
            return payload
        # 200 but not the expected JSON (bot-challenge page) -> fall back.
    except Exception as exc:  # noqa: BLE001 - any live failure falls back to Wayback
        print(f"[ioc] live origin failed for {comp}: {type(exc).__name__}: {exc}; using Wayback")
    payload = _wayback_latest(comp)
    if not (isinstance(payload, dict) and isinstance(payload.get("medalNOC"), list)):
        raise RuntimeError(f"unexpected CIS_MedalNOCs shape for {comp}")
    return payload


def _to_int(v):
    return int(v) if v is not None and v != "" else None


def fetch_medal_table(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    rows = []
    for comp, games in EDITIONS:
        payload = _fetch_medal_payload(comp)
        for r in payload["medalNOC"]:
            org = r.get("organisation") or {}
            rows.append({
                "edition": comp,
                "games": games,
                "noc_code": r.get("org") or org.get("code"),
                "noc_name": org.get("description"),
                "sport": r.get("sport"),
                "gender": r.get("gender"),
                "gold": _to_int(r.get("gold")),
                "silver": _to_int(r.get("silver")),
                "bronze": _to_int(r.get("bronze")),
                "total": _to_int(r.get("total")),
                "rank": _to_int(r.get("rank")),
                "rank_total": _to_int(r.get("rankTotal")),
            })
    if not rows:
        raise RuntimeError("ioc-medal-table: no rows fetched from any edition")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="ioc-medal-table", fn=fetch_medal_table, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ioc-medal-table-transform",
        deps=["ioc-medal-table"],
        sql='''
            SELECT
                edition,
                games,
                noc_code,
                noc_name,
                sport,
                gender,
                CAST(gold   AS BIGINT) AS gold,
                CAST(silver AS BIGINT) AS silver,
                CAST(bronze AS BIGINT) AS bronze,
                CAST(total  AS BIGINT) AS total,
                CAST(rank   AS BIGINT) AS rank,
                CAST(rank_total AS BIGINT) AS rank_total
            FROM "ioc-medal-table"
            WHERE noc_code IS NOT NULL
              AND sport IS NOT NULL
              AND gender IS NOT NULL
        ''',
        key=("edition", "noc_code", "sport", "gender"),
    ),
]
