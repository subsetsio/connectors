"""IOC (olympics.com) connector.

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
from json import JSONDecodeError

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    save_raw_parquet,
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


def _response_json(resp) -> object | None:
    try:
        return resp.json()
    except JSONDecodeError as exc:
        print(f"[ioc] skipped non-JSON response from {resp.url}: {exc}")
        return None


def _live_url(comp: str) -> str:
    return f"https://olympics.com/{comp}/data/CIS_MedalNOCs~lang=ENG~comp={comp}.json"


def _cdx_latest(prefix: str, comp: str, languages: tuple[str, ...] = ("ENG",)) -> list[tuple[str, str]]:
    """Return latest Wayback timestamp per archived ODF URL under `prefix`."""
    latest: dict[str, str] = {}

    # The Wayback corpus is not path-consistent: several PG2024 JSON files are
    # archived below /OG2024/data/ while carrying comp=PG2024 in the filename.
    for path_comp, _games in EDITIONS:
        try:
            resp = get(
                "https://web.archive.org/cdx/search/cdx",
                params={
                    "url": f"olympics.com/{path_comp}/data/{prefix}",
                    "matchType": "prefix",
                    "output": "json",
                    "fl": "timestamp,original",
                    "filter": "statuscode:200",
                    "collapse": "urlkey",
                },
                timeout=(10.0, 120.0),
            )
            resp.raise_for_status()
            data = _response_json(resp)
        except Exception as exc:  # noqa: BLE001 - CDX is a best-effort archive index.
            print(f"[ioc] CDX search failed for {path_comp}/{prefix}: {type(exc).__name__}: {exc}")
            continue
        if not isinstance(data, list) or len(data) < 2:
            continue
        for ts, orig in data[1:]:
            if "%7B" in orig or "{code}" in orig:
                continue
            if f"comp={comp}" not in orig:
                continue
            if languages and not any(f"lang={lang}" in orig for lang in languages):
                continue
            if ts > latest.get(orig, ""):
                latest[orig] = ts
    return [(ts, orig) for orig, ts in sorted(latest.items())]


def _wayback_latest(comp: str) -> dict:
    """Newest archived CIS_MedalNOCs (ENG) snapshot for `comp`, via CDX + id_."""
    cands = _cdx_latest("CIS_MedalNOCs", comp)
    if not cands:
        raise RuntimeError(f"no archived CIS_MedalNOCs ENG snapshot for {comp}")
    # Prefer the final frozen table, but archive payload fetches can time out.
    # Walk backward through captures so one flaky archived body does not fail
    # the entire immutable Games edition.
    last_exc: Exception | None = None
    for ts, orig in sorted(cands, reverse=True):
        try:
            return _get_json(f"https://web.archive.org/web/{ts}id_/{orig}")
        except Exception as exc:  # noqa: BLE001 - Wayback payload fetch is best effort.
            last_exc = exc
            print(f"[ioc] archived medal payload failed {orig} at {ts}: {type(exc).__name__}: {exc}")
    raise RuntimeError(f"no readable archived CIS_MedalNOCs ENG snapshot for {comp}") from last_exc


def _wayback_json(ts: str, orig: str) -> dict:
    return _get_json(f"https://web.archive.org/web/{ts}id_/{orig}")


def _try_wayback_json(ts: str, orig: str) -> dict | None:
    try:
        return _wayback_json(ts, orig)
    except JSONDecodeError as exc:
        print(f"[ioc] skipped non-JSON archived payload {orig} at {ts}: {exc}")
        return None
    except Exception as exc:  # noqa: BLE001 - one archived entity timing out should not abort the corpus.
        print(f"[ioc] skipped archived payload {orig} at {ts}: {type(exc).__name__}: {exc}")
        return None


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


def fetch_disciplines(node_id: str) -> None:
    rows = []
    for comp, games in EDITIONS:
        cands = _cdx_latest("GLO_Disciplines", comp, languages=("ENG", "EN"))
        if not cands:
            print(f"[ioc] no archived GLO_Disciplines payloads for {comp}; skipping")
            continue
        ts, orig = max(cands, key=lambda x: x[0])
        payload = _wayback_json(ts, orig)
        rows.append({
            "edition": comp,
            "games": games,
            "source_url": orig,
            "archive_timestamp": ts,
            "payload": payload,
        })
    if not rows:
        raise RuntimeError("ioc-disciplines: no archived discipline payloads fetched")
    save_raw_ndjson(rows, node_id)


def fetch_nocs(node_id: str) -> None:
    rows = []
    for comp, games in EDITIONS:
        for ts, orig in _cdx_latest("GLO_NocBio", comp):
            payload = _try_wayback_json(ts, orig)
            noc = (payload or {}).get("nocBio") or {}
            noc_code = noc.get("organisationId") or _extract_url_field(orig, "organisation")
            if payload is None and noc_code:
                # The CDX URL is itself the frozen NOC catalog entry. Keep the
                # row when the archived body is transiently unavailable so a
                # few Wayback timeouts do not collapse the reference corpus.
                payload = {"nocBio": {"organisationId": noc_code}}
            rows.append({
                "edition": comp,
                "games": games,
                "noc_code": noc_code,
                "source_url": orig,
                "archive_timestamp": ts,
                "payload": payload,
            })
    if not rows:
        raise RuntimeError("ioc-nocs: no archived NOC biography payloads fetched")
    save_raw_ndjson(rows, node_id)


def _extract_event_code(orig: str) -> str | None:
    marker = "~event="
    if marker not in orig:
        return None
    return orig.split(marker, 1)[1].split("~", 1)[0]


def fetch_event_results(node_id: str) -> None:
    rows = []
    for comp, games in EDITIONS:
        for ts, orig in _cdx_latest("GLO_EventRanking", comp):
            payload = _try_wayback_json(ts, orig)
            if payload is None:
                continue
            rows.append({
                "edition": comp,
                "games": games,
                "event_code": _extract_event_code(orig),
                "source_url": orig,
                "archive_timestamp": ts,
                "payload": payload,
            })
    if not rows:
        raise RuntimeError("ioc-event-results: no archived event ranking payloads fetched")
    save_raw_ndjson(rows, node_id)


def _extract_athlete_code(orig: str) -> str | None:
    marker = "~code="
    if marker not in orig:
        return None
    return orig.split(marker, 1)[1].split("~", 1)[0]


def _extract_url_field(orig: str, field: str) -> str | None:
    marker = f"~{field}="
    if marker not in orig:
        return None
    return orig.split(marker, 1)[1].split("~", 1)[0].split(".", 1)[0]


def fetch_athletes(node_id: str) -> None:
    rows = []
    for comp, games in EDITIONS:
        for ts, orig in _cdx_latest("CIS_Bio_Athlete", comp):
            payload = _try_wayback_json(ts, orig)
            if payload is None:
                continue
            person = payload.get("person") or {}
            rows.append({
                "edition": comp,
                "games": games,
                "athlete_code": person.get("code") or _extract_athlete_code(orig),
                "source_url": orig,
                "archive_timestamp": ts,
                "payload": payload,
            })
    if not rows:
        raise RuntimeError("ioc-athletes: no archived athlete biography payloads fetched")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ioc-athletes", fn=fetch_athletes, kind="download"),
    NodeSpec(id="ioc-disciplines", fn=fetch_disciplines, kind="download"),
    NodeSpec(id="ioc-event-results", fn=fetch_event_results, kind="download"),
    NodeSpec(id="ioc-medal-table", fn=fetch_medal_table, kind="download"),
    NodeSpec(id="ioc-nocs", fn=fetch_nocs, kind="download"),
]
