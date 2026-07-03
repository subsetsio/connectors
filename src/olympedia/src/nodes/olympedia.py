"""Olympedia connector — node module.

Olympedia (www.olympedia.org) is a server-rendered static-HTML database of
Olympic history. There is no API, no JSON, no bulk/CSV export — every dataset
is parsed out of HTML <table> markup in the initial response (no JS). See the
research asset for the full surface.

Fetch shape: **stateless full re-pull** (the corpus is near-static historical
data that only changes when a new Games is added). Each fetch fn scrapes its
page(s), parses rows to plain JSON-native values (strings for everything; the
SQL transforms own typing via CAST), and overwrites one raw ndjson asset. No
watermarks/cursors — a full re-pull is cheap (most assets are one request;
medal_table_by_edition is ~75 and olympic_records ~5).

Politeness: robots.txt mandates `Crawl-delay: 10`. Single-page assets make one
request. The two multi-page assets sleep REQUEST_DELAY between requests to stay
within the crawl budget and avoid blocks.
"""
import io
import re
import time

import pandas as pd  # noqa: F401  (kept available; parsing uses lxml directly)
import lxml.html as LH

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)

BASE = "https://www.olympedia.org"
REQUEST_DELAY = 10  # seconds — honour robots Crawl-delay between requests in loops


@transient_retry()  # 6 attempts, exponential backoff over transient/429/5xx
def _get(path: str) -> str:
    resp = get(BASE + path, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _doc(path: str):
    return LH.fromstring(_get(path))


def _txt(el) -> str | None:
    """Cleaned text content of an element, or None if empty."""
    t = " ".join(s.strip() for s in el.itertext() if s.strip())
    return t or None


def _int(s):
    """int() of a clean (optionally signed) integer string, else None."""
    if s is None:
        return None
    s = str(s).strip().replace(",", "")
    return int(s) if re.fullmatch(r"-?\d+", s) else None


def _ints_in_row(tds) -> list[int]:
    """Return the integer values of cells in a row whose text is a plain integer."""
    out = []
    for c in tds:
        s = (c.text_content() or "").strip().replace(",", "")
        if re.fullmatch(r"-?\d+", s):
            out.append(int(s))
    return out


def _host_noc_from_row(row):
    """Host NOC code from the flag <img> in an /editions row (src .../<CODE>.svg)."""
    for src in row.xpath('.//img/@src'):
        m = re.search(r"olympedia-flags.*/([A-Za-z]{2,4})\.svg$", src)
        if m:
            return m.group(1)
    return None


def _noc_from_row(row):
    """Extract (noc_code, country_name) from the first /countries/<CODE> link in a row."""
    code = name = None
    for a in row.xpath('.//a[contains(@href,"/countries/")]'):
        m = re.search(r"/countries/([A-Za-z]{2,4})$", a.get("href") or "")
        if m and code is None:
            code = m.group(1)
        t = (a.text_content() or "").strip()
        if t and name is None:
            name = t
    return code, name


# ---------------------------------------------------------------------------
# Reference dimensions
# ---------------------------------------------------------------------------

# h2 sections of /editions we treat as real Olympic editions (skip Forerunners
# and Ancient Olympic Games — pre-modern, no comparable medal tables).
EDITION_CATEGORIES = {
    "Olympic Games",
    "Intercalated Games",
    "Youth Olympic Games",
}


def _parse_editions(doc):
    """Walk /editions in document order, tracking h2 (category) and h3 (season).
    Yield dicts for editions in EDITION_CATEGORIES with a numeric /editions/<id>."""
    body = doc.body if doc.body is not None else doc
    category = None
    season = None
    rows_out = []
    for el in body.iter():
        tag = el.tag
        if not isinstance(tag, str):
            continue
        if tag == "h2":
            category = _txt(el)
            season = None
        elif tag == "h3":
            season = _txt(el)
        elif tag == "table":
            if category not in EDITION_CATEGORIES:
                continue
            for tr in el.xpath(".//tr"):
                ids = [
                    h for h in tr.xpath('.//a/@href')
                    if re.search(r"/editions/\d+$", h)
                ]
                if not ids:
                    continue
                tds = tr.xpath("./td")
                if len(tds) < 7:
                    continue
                edition_id = int(re.search(r"/editions/(\d+)$", ids[0]).group(1))
                host_noc = _host_noc_from_row(tr)
                rows_out.append({
                    "edition_id": edition_id,
                    "category": category,
                    "season": season,
                    "year": _int((tds[1].text_content() or "").strip()),
                    "city": _txt(tds[2]),
                    "host_noc": host_noc,
                    "opened": _txt(tds[4]),
                    "closed": _txt(tds[5]),
                    "competition": _txt(tds[6]),
                })
    return rows_out


def fetch_editions(node_id: str) -> None:
    asset = node_id
    rows = _parse_editions(_doc("/editions"))
    save_raw_ndjson(rows, asset)


def fetch_countries(node_id: str) -> None:
    asset = node_id
    doc = _doc("/countries")
    tables = doc.xpath("//table")
    rows = []
    # table[0] = modern NOCs, table[1] = ancient countries (both: Abbr, Country, status glyph)
    for section, tbl in zip(("modern", "ancient"), tables[:2]):
        for tr in tbl.xpath(".//tr"):
            tds = tr.xpath("./td")
            if len(tds) < 2:
                continue
            code = (tds[0].text_content() or "").strip()
            country = (tds[1].text_content() or "").strip()
            if not code or not country:
                continue
            glyph = LH.tostring(tds[2], encoding="unicode") if len(tds) >= 3 else ""
            rows.append({
                "noc_code": code,
                "country": country,
                "competed_modern": "glyphicon-ok" in glyph,
                "section": section,
            })
    save_raw_ndjson(rows, asset)


def fetch_sports(node_id: str) -> None:
    asset = node_id
    doc = _doc("/sports")
    tbl = doc.xpath("//table")[0]
    rows = []
    for tr in tbl.xpath(".//tr"):
        tds = tr.xpath("./td")
        if len(tds) < 4:
            continue
        code = (tds[0].text_content() or "").strip()
        discipline = (tds[1].text_content() or "").strip()
        if not code or not discipline:
            continue
        glyph = LH.tostring(tds[4], encoding="unicode") if len(tds) >= 5 else ""
        rows.append({
            "discipline_code": code,
            "discipline": discipline,
            "sport": (tds[2].text_content() or "").strip() or None,
            "season": (tds[3].text_content() or "").strip() or None,
            "olympic_status": "glyphicon-ok" in glyph,
        })
    save_raw_ndjson(rows, asset)


# ---------------------------------------------------------------------------
# Pre-aggregated all-time statistics (one page each)
# ---------------------------------------------------------------------------

def _simple_stat_rows(path, colmap):
    """Parse the first <table> of a statistics page positionally.

    colmap: list of (output_key, td_index) — text is extracted at that index.
    Returns rows skipping the header and any row too short.
    """
    doc = _doc(path)
    tbl = doc.xpath("//table")[0]
    max_idx = max(i for _, i in colmap)
    rows = []
    for tr in tbl.xpath(".//tr"):
        tds = tr.xpath("./td")
        if len(tds) <= max_idx:
            continue
        rows.append({k: ((tds[i].text_content() or "").strip() or None) for k, i in colmap})
    return rows


def fetch_medals_by_country(node_id: str) -> None:
    # cols: NOC(flag), NOC(name+code link), Gold, Silver, Bronze, Total
    doc = _doc("/statistics/medal/country")
    tbl = doc.xpath("//table")[0]
    rows = []
    for tr in tbl.xpath(".//tr"):
        tds = tr.xpath("./td")
        if len(tds) < 5:
            continue
        code, name = _noc_from_row(tr)
        nums = _ints_in_row(tds)
        if not code or len(nums) < 4:
            continue
        g, s, b, total = nums[-4:]
        rows.append({
            "noc_code": code, "country": name,
            "gold": g, "silver": s, "bronze": b, "total": total,
        })
    save_raw_ndjson(rows, node_id)


def fetch_medals_by_athlete(node_id: str) -> None:
    # cols: Athlete, Nat, Gold, Silver, Bronze, Total
    rows = _simple_stat_rows("/statistics/medal/athlete", [
        ("athlete", 0), ("noc_code", 1),
        ("gold", 2), ("silver", 3), ("bronze", 4), ("total", 5),
    ])
    for r in rows:
        for k in ("gold", "silver", "bronze", "total"):
            r[k] = _int(r[k])
    save_raw_ndjson(rows, node_id)


def fetch_participations(node_id: str) -> None:
    # cols: Athlete, Nation(s), Sport(s), Role(s), Era, Participations
    rows = _simple_stat_rows("/statistics/participation", [
        ("athlete", 0), ("nations", 1), ("sports", 2),
        ("roles", 3), ("era", 4), ("participations", 5),
    ])
    for r in rows:
        r["participations"] = _int(r["participations"])
    save_raw_ndjson(rows, node_id)


def fetch_age_records(node_id: str) -> None:
    # cols: Athlete, Born, NOC, Discipline (Sport), Event, Dates, Placement, Age
    rows = _simple_stat_rows("/statistics/age", [
        ("athlete", 0), ("born", 1), ("noc_code", 2), ("discipline_sport", 3),
        ("event", 4), ("dates", 5), ("placement", 6), ("age", 7),
    ])
    save_raw_ndjson(rows, node_id)


# ---------------------------------------------------------------------------
# Multi-page derived corpora
# ---------------------------------------------------------------------------

def _find_medal_table(doc):
    """The per-edition medal-by-NOC table: header includes NOC/Gold/Silver/Bronze/Total
    and is NOT the 'most successful competitors' athlete table (which has 'Athlete')."""
    for tbl in doc.xpath("//table"):
        heads = [th.text_content().strip() for th in tbl.xpath(".//tr[1]//th")]
        if "NOC" in heads and "Gold" in heads and "Total" in heads and "Athlete" not in heads:
            return tbl
    return None


def fetch_medal_table_by_edition(node_id: str) -> None:
    asset = node_id
    editions = _parse_editions(_doc("/editions"))
    rows = []
    for ed in editions:
        time.sleep(REQUEST_DELAY)
        doc = _doc(f"/editions/{ed['edition_id']}")
        tbl = _find_medal_table(doc)
        if tbl is None:
            continue  # future edition / no medals yet
        for tr in tbl.xpath(".//tr"):
            tds = tr.xpath("./td")
            if len(tds) < 5:
                continue
            code, name = _noc_from_row(tr)
            nums = _ints_in_row(tds)
            if not code or len(nums) < 4:
                continue  # skip totals/blank rows
            g, s, b, total = nums[-4:]
            rows.append({
                "edition_id": ed["edition_id"],
                "year": ed["year"],
                "season": ed["season"],
                "category": ed["category"],
                "noc_code": code, "country": name,
                "gold": g, "silver": s, "bronze": b, "total": total,
            })
    save_raw_ndjson(rows, asset)


def fetch_olympic_records(node_id: str) -> None:
    asset = node_id
    index = _doc("/records")
    disciplines = {}  # code -> name
    for a in index.xpath('//a[contains(@href,"/records/sport/")]'):
        m = re.search(r"/records/sport/([A-Za-z0-9]+)$", a.get("href") or "")
        if m:
            disciplines[m.group(1)] = (a.text_content() or "").strip() or None
    rows = []
    for code, name in disciplines.items():
        time.sleep(REQUEST_DELAY)
        doc = _doc(f"/records/sport/{code}")
        tables = doc.xpath("//table")
        if not tables:
            continue
        # table[0] = current records; cols: Event, Current Record, Athlete(s),
        # NOC, Games, Date, Phase, Rank
        for tr in tables[0].xpath(".//tr"):
            tds = tr.xpath("./td")
            if len(tds) < 8:
                continue
            rows.append({
                "discipline_code": code,
                "discipline": name,
                "event": (tds[0].text_content() or "").strip() or None,
                "current_record": (tds[1].text_content() or "").strip() or None,
                "athletes": (tds[2].text_content() or "").strip() or None,
                "noc_code": (tds[3].text_content() or "").strip() or None,
                "games": (tds[4].text_content() or "").strip() or None,
                "date": (tds[5].text_content() or "").strip() or None,
                "phase": (tds[6].text_content() or "").strip() or None,
                "rank": (tds[7].text_content() or "").strip() or None,
            })
    save_raw_ndjson(rows, asset)


# ---------------------------------------------------------------------------
# DOWNLOAD_SPECS — one per entity-union entry
# ---------------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="olympedia-editions", fn=fetch_editions, kind="download"),
    NodeSpec(id="olympedia-countries", fn=fetch_countries, kind="download"),
    NodeSpec(id="olympedia-sports", fn=fetch_sports, kind="download"),
    NodeSpec(id="olympedia-medals-by-country", fn=fetch_medals_by_country, kind="download"),
    NodeSpec(id="olympedia-medals-by-athlete", fn=fetch_medals_by_athlete, kind="download"),
    NodeSpec(id="olympedia-participations", fn=fetch_participations, kind="download"),
    NodeSpec(id="olympedia-age-records", fn=fetch_age_records, kind="download"),
    NodeSpec(id="olympedia-medal-table-by-edition", fn=fetch_medal_table_by_edition, kind="download"),
    NodeSpec(id="olympedia-olympic-records", fn=fetch_olympic_records, kind="download"),
]


# ---------------------------------------------------------------------------
# TRANSFORM_SPECS — one published Delta table per subset
# ---------------------------------------------------------------------------

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="olympedia-editions-transform",
        deps=["olympedia-editions"],
        key=("edition_id",),
        temporal="year",
        sql='''
            SELECT
                CAST(edition_id AS INTEGER) AS edition_id,
                category,
                season,
                TRY_CAST(year AS INTEGER)   AS year,
                city,
                host_noc,
                opened,
                closed,
                competition
            FROM "olympedia-editions"
            WHERE edition_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="olympedia-countries-transform",
        deps=["olympedia-countries"],
        key=("noc_code",),
        sql='''
            SELECT
                noc_code,
                country,
                CAST(competed_modern AS BOOLEAN) AS competed_modern,
                section
            FROM "olympedia-countries"
            WHERE noc_code IS NOT NULL AND country IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="olympedia-sports-transform",
        deps=["olympedia-sports"],
        key=("discipline_code",),
        sql='''
            SELECT
                discipline_code,
                discipline,
                sport,
                season,
                CAST(olympic_status AS BOOLEAN) AS olympic_status
            FROM "olympedia-sports"
            WHERE discipline_code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="olympedia-medals-by-country-transform",
        deps=["olympedia-medals-by-country"],
        key=("noc_code",),
        sql='''
            SELECT
                noc_code,
                country,
                CAST(gold AS INTEGER)   AS gold,
                CAST(silver AS INTEGER) AS silver,
                CAST(bronze AS INTEGER) AS bronze,
                CAST(total AS INTEGER)  AS total
            FROM "olympedia-medals-by-country"
            WHERE noc_code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="olympedia-medals-by-athlete-transform",
        deps=["olympedia-medals-by-athlete"],
        key=("athlete",),
        sql='''
            SELECT
                athlete,
                noc_code,
                CAST(gold AS INTEGER)   AS gold,
                CAST(silver AS INTEGER) AS silver,
                CAST(bronze AS INTEGER) AS bronze,
                CAST(total AS INTEGER)  AS total
            FROM "olympedia-medals-by-athlete"
            WHERE athlete IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="olympedia-participations-transform",
        deps=["olympedia-participations"],
        key=("athlete",),
        sql='''
            SELECT
                athlete,
                nations,
                sports,
                roles,
                era,
                TRY_CAST(participations AS INTEGER) AS participations
            FROM "olympedia-participations"
            WHERE athlete IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="olympedia-age-records-transform",
        deps=["olympedia-age-records"],
        sql='''
            SELECT
                athlete,
                born,
                noc_code,
                discipline_sport,
                event,
                dates,
                placement,
                age
            FROM "olympedia-age-records"
            WHERE athlete IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="olympedia-medal-table-by-edition-transform",
        deps=["olympedia-medal-table-by-edition"],
        key=("edition_id", "noc_code"),
        temporal="year",
        sql='''
            SELECT
                CAST(edition_id AS INTEGER) AS edition_id,
                TRY_CAST(year AS INTEGER)   AS year,
                season,
                category,
                noc_code,
                country,
                CAST(gold AS INTEGER)   AS gold,
                CAST(silver AS INTEGER) AS silver,
                CAST(bronze AS INTEGER) AS bronze,
                CAST(total AS INTEGER)  AS total
            FROM "olympedia-medal-table-by-edition"
            WHERE edition_id IS NOT NULL AND noc_code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="olympedia-olympic-records-transform",
        deps=["olympedia-olympic-records"],
        sql='''
            SELECT
                discipline_code,
                discipline,
                event,
                current_record,
                athletes,
                noc_code,
                games,
                date,
                phase,
                rank
            FROM "olympedia-olympic-records"
            WHERE event IS NOT NULL
        ''',
    ),
]
