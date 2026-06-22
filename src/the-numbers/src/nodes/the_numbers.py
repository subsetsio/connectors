"""The Numbers (the-numbers.com) connector.

Scrapes the free, server-rendered box-office chart tables — the only free,
verifiable surface (the machine-readable OpusData feed is paid/license-gated).
Four published subsets, each a date-partitioned time series:

  - daily-box-office     one row per movie per calendar day
  - weekend-box-office   one row per movie per weekend (Fri-Sun)
  - weekly-box-office    one row per movie per week
  - annual-top-grossing  one row per movie per release year (annual market page)

The three chart series are walked via each page's own prev/next navigation
links — no hardcoded date ranges; the chain itself defines the period set.
They use a year-bucketed firehose shape: raw is written one parquet per
calendar year (`<node>-<year>`), state tracks how far backfill has reached, and
the most-recent year is always re-fetched to pick up new dates and revisions.
The full ~30-year daily history is ~10k pages; per-year raw+state writes make a
supervisor interrupt safe to resume from the saved frontier. The annual market
table is tiny (~30 pages) so it uses a stateless full re-pull each run.

LICENSING NOTE (curator): the site's terms reserve systematic scraping to
licensed OpusData customers; robots.txt does not block general crawlers. This
is a redistribution/ToS concern flagged at research, not a technical one.
"""
import datetime
import re

import lxml.html
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    load_state,
    save_state,
)

STATE_VERSION = 1
BASE = "https://www.the-numbers.com"

# node id -> chart kind (the URL segment and the prev/next link namespace)
CHART_KINDS = {
    "the-numbers-daily-box-office": "daily",
    "the-numbers-weekend-box-office": "weekend",
    "the-numbers-weekly-box-office": "weekly",
}
LANDING = {
    "daily": "/daily-box-office-chart",
    "weekend": "/weekend-box-office-chart",
    "weekly": "/weekly-box-office-chart",
}

# One unified schema across all three charts. Daily pages carry a separate
# DailyChange column; weekend/weekly do not — that column is just null for them.
CHART_SCHEMA = pa.schema([
    ("chart_date", pa.string()),        # ISO YYYY-MM-DD of the chart page
    ("rank", pa.int64()),
    ("prev_rank", pa.int64()),
    ("title", pa.string()),
    ("gross", pa.int64()),
    ("daily_change_pct", pa.float64()),
    ("weekly_change_pct", pa.float64()),
    ("theaters", pa.int64()),
    ("theater_average", pa.int64()),
    ("total_gross", pa.int64()),
    ("days_in_release", pa.int64()),
])

ANNUAL_SCHEMA = pa.schema([
    ("year", pa.int64()),
    ("rank", pa.int64()),
    ("title", pa.string()),
    ("release_date", pa.string()),
    ("distributor", pa.string()),
    ("genre", pa.string()),
    ("gross", pa.int64()),
    ("tickets_sold", pa.int64()),
])


# --- HTTP -------------------------------------------------------------------

@transient_retry()
def _get_html(path):
    """GET a page; return its text, or None on a 404 (a missing chart date /
    end of the link chain — a permanent 'not found', not a transient error)."""
    url = path if path.startswith("http") else BASE + path
    r = get(url, timeout=(10.0, 120.0))
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.text


# --- parsing ----------------------------------------------------------------

def _norm(s):
    return re.sub(r"\s+", " ", (s or "").replace("\xa0", " ")).strip()


def _clean(s):
    return _norm(s) or None


def _int(s):
    m = re.search(r"-?\d[\d,]*", _norm(s))
    return int(m.group(0).replace(",", "")) if m else None


def _money(s):
    m = re.search(r"-?\d[\d,]*", _norm(s))
    return int(m.group(0).replace(",", "")) if m else None


def _pct(s):
    m = re.search(r"-?\d[\d.,]*", _norm(s))
    return float(m.group(0).replace(",", "")) if m else None


def _date_re(kind):
    return re.compile(rf"/box-office-chart/{kind}/(\d{{4}})/(\d{{2}})/(\d{{2}})")


def _path(kind, date):
    return f"/box-office-chart/{kind}/{date}"          # date = "YYYY/MM/DD"


def _iso(date):
    return date.replace("/", "-")


def _neighbours(doc, kind, cur_date):
    """Return (prev_date, next_date) chart dates from the page's nav links,
    distinguishing prev/next purely by ordering against the current date."""
    pat = _date_re(kind)
    found = sorted({
        f"{m.group(1)}/{m.group(2)}/{m.group(3)}"
        for a in doc.xpath("//a/@href")
        for m in [pat.search(a)] if m
    })
    prevs = [d for d in found if d < cur_date]
    nexts = [d for d in found if d > cur_date]
    return (max(prevs) if prevs else None,
            min(nexts) if nexts else None)


def _parse_chart(html, kind, cur_date):
    """Parse one chart page. Returns (rows, prev_date, next_date).

    The page renders the table twice (responsive desktop+mobile copies); we
    take only the first matching table so rows are not duplicated.
    """
    doc = lxml.html.fromstring(html)
    rows = []
    for table in doc.xpath("//table"):
        trs = table.xpath(".//tr")
        if len(trs) < 2:
            continue
        hdr = [_norm(c.text_content()) for c in trs[0].xpath("./th|./td")]
        if "Rank" not in hdr or "Title" not in hdr:
            continue
        idx = {h: i for i, h in enumerate(hdr)}

        def cell(texts, name):
            i = idx.get(name)
            return texts[i] if (i is not None and i < len(texts)) else None

        for tr in trs[1:]:
            cells = tr.xpath("./td|./th")
            if len(cells) < len(hdr):
                continue
            t = [c.text_content() for c in cells]
            title = _clean(cell(t, "Title"))
            if not title:
                continue
            rows.append({
                "chart_date": _iso(cur_date),
                "rank": _int(cell(t, "Rank")),
                "prev_rank": _int(cell(t, "Prev")),
                "title": title,
                "gross": _money(cell(t, "Gross")),
                "daily_change_pct": _pct(cell(t, "DailyChange")),
                "weekly_change_pct": _pct(cell(t, "WeeklyChange")),
                "theaters": _int(cell(t, "Theaters")),
                "theater_average": _money(cell(t, "TheaterAverage")),
                "total_gross": _money(cell(t, "Total Gross")),
                "days_in_release": _int(cell(t, "Days in Release")),
            })
        break  # first matching table only

    prev_date, next_date = _neighbours(doc, kind, cur_date)
    return rows, prev_date, next_date


def _parse_annual(html, year):
    doc = lxml.html.fromstring(html)
    for table in doc.xpath("//table"):
        trs = table.xpath(".//tr")
        if len(trs) < 2:
            continue
        hdr = [_norm(c.text_content()) for c in trs[0].xpath("./th|./td")]
        if "Movie" not in hdr or "Rank" not in hdr:
            continue
        idx = {h: i for i, h in enumerate(hdr)}
        gross_i = next((i for h, i in idx.items() if "Gross" in h), None)
        out = []
        for tr in trs[1:]:
            cells = [c.text_content() for c in tr.xpath("./td|./th")]
            if len(cells) < len(hdr):
                continue
            title = _clean(cells[idx["Movie"]])
            if not title:
                continue
            out.append({
                "year": year,
                "rank": _int(cells[idx["Rank"]]),
                "title": title,
                "release_date": _clean(cells[idx["Release Date"]]) if "Release Date" in idx else None,
                "distributor": _clean(cells[idx["Distributor"]]) if "Distributor" in idx else None,
                "genre": _clean(cells[idx["Genre"]]) if "Genre" in idx else None,
                "gross": _money(cells[gross_i]) if gross_i is not None else None,
                "tickets_sold": _int(cells[idx["Tickets Sold"]]) if "Tickets Sold" in idx else None,
            })
        return out
    return []


# --- chart fetch (firehose, year-bucketed, link-walked) ---------------------

def _latest_link(html, kind):
    pat = _date_re(kind)
    found = sorted({
        f"{m.group(1)}/{m.group(2)}/{m.group(3)}"
        for a in lxml.html.fromstring(html).xpath("//a/@href")
        for m in [pat.search(a)] if m
    })
    return found[-1] if found else None


def _find_newest(kind):
    """Discover the newest dated chart page by seeding from the landing page's
    latest date link and walking forward via next links to the live edge."""
    html = _get_html(LANDING[kind])
    if html is None:
        return None
    cur = _latest_link(html, kind)
    if cur is None:
        return None
    last_good = None
    while True:
        page = _get_html(_path(kind, cur))
        if page is None:
            return last_good
        last_good = cur
        _, _, next_date = _parse_chart(page, kind, cur)
        if next_date is None:
            return cur
        cur = next_date


def _fetch_year_backward(node_id, kind, start_date):
    """Walk backward from start_date collecting every chart page whose year
    matches start_date's year, write that year's parquet bucket (overwrite),
    and return the first older date (frontier for the next year) or None when
    the chain ends. Re-fetching a whole year and overwriting keeps it
    idempotent and resumable after interruption."""
    year = start_date[:4]
    rows = []
    cur = start_date
    while cur is not None and cur[:4] == year:
        html = _get_html(_path(kind, cur))
        if html is None:
            cur = None
            break
        page_rows, prev_date, _ = _parse_chart(html, kind, cur)
        rows.extend(page_rows)
        cur = prev_date
    if rows:
        save_raw_parquet(pa.Table.from_pylist(rows, schema=CHART_SCHEMA),
                         f"{node_id}-{year}")
    return cur  # first date with year < target, or None at chain start


def fetch_chart(node_id):
    kind = CHART_KINDS[node_id]
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {"schema_version": STATE_VERSION}

    # 1) Refresh: always re-fetch the most-recent (current) year in full so new
    #    dates and revised estimates are picked up; overwrite its bucket.
    newest = _find_newest(kind)
    if newest is None:
        raise RuntimeError(f"{node_id}: could not locate newest {kind} chart")
    frontier_seed = _fetch_year_backward(node_id, kind, newest)
    state["newest_seen"] = newest
    if "frontier" not in state:
        state["frontier"] = frontier_seed   # first run seeds the backfill cursor
    save_state(node_id, state)

    # 2) Backfill older years from the stored frontier, one durable year at a
    #    time. Loops until the chain's start (no older page). The supervisor
    #    bounds wall-clock; the per-year raw+state writes make that safe.
    cursor = state.get("frontier")
    while cursor:
        prev_year = cursor[:4]
        next_cursor = _fetch_year_backward(node_id, kind, cursor)
        if next_cursor is not None and next_cursor[:4] >= prev_year:
            raise RuntimeError(
                f"{node_id}: backfill cursor failed to advance "
                f"({cursor} -> {next_cursor})"
            )
        cursor = next_cursor
        state["frontier"] = cursor
        save_state(node_id, state)


# --- annual fetch (stateless full re-pull) ----------------------------------

def fetch_annual(node_id):
    year = datetime.datetime.now().year
    rows = []
    misses = 0
    while year >= 1900:
        html = _get_html(f"/market/{year}/top-grossing-movies")
        year_rows = _parse_annual(html, year) if html else []
        if year_rows:
            rows.extend(year_rows)
            misses = 0
        else:
            misses += 1
            if misses >= 2:        # two consecutive empty years -> chain start
                break
        year -= 1
    else:
        raise RuntimeError(f"{node_id}: annual walk underflowed past 1900")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=ANNUAL_SCHEMA), node_id)


# --- specs ------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="the-numbers-daily-box-office", fn=fetch_chart, kind="download"),
    NodeSpec(id="the-numbers-weekend-box-office", fn=fetch_chart, kind="download"),
    NodeSpec(id="the-numbers-weekly-box-office", fn=fetch_chart, kind="download"),
    NodeSpec(id="the-numbers-annual-top-grossing", fn=fetch_annual, kind="download"),
]

_CHART_COLS_COMMON = """
    CAST(chart_date AS DATE)          AS date,
    CAST(rank AS INTEGER)             AS rank,
    CAST(prev_rank AS INTEGER)        AS prev_rank,
    title,
    CAST(gross AS BIGINT)             AS gross,
    CAST(weekly_change_pct AS DOUBLE) AS weekly_change_pct,
    CAST(theaters AS INTEGER)         AS theaters,
    CAST(theater_average AS BIGINT)   AS theater_average,
    CAST(total_gross AS BIGINT)       AS total_gross,
    CAST(days_in_release AS INTEGER)  AS days_in_release
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="the-numbers-daily-box-office-transform",
        deps=["the-numbers-daily-box-office"],
        sql=f'''
            SELECT
                CAST(chart_date AS DATE)            AS date,
                CAST(rank AS INTEGER)               AS rank,
                CAST(prev_rank AS INTEGER)          AS prev_rank,
                title,
                CAST(gross AS BIGINT)               AS gross,
                CAST(daily_change_pct AS DOUBLE)    AS daily_change_pct,
                CAST(weekly_change_pct AS DOUBLE)   AS weekly_change_pct,
                CAST(theaters AS INTEGER)           AS theaters,
                CAST(theater_average AS BIGINT)     AS theater_average,
                CAST(total_gross AS BIGINT)         AS total_gross,
                CAST(days_in_release AS INTEGER)    AS days_in_release
            FROM "the-numbers-daily-box-office"
            WHERE title IS NOT NULL AND gross IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY chart_date, title ORDER BY total_gross DESC
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="the-numbers-weekend-box-office-transform",
        deps=["the-numbers-weekend-box-office"],
        sql=f'''
            SELECT {_CHART_COLS_COMMON}
            FROM "the-numbers-weekend-box-office"
            WHERE title IS NOT NULL AND gross IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY chart_date, title ORDER BY total_gross DESC
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="the-numbers-weekly-box-office-transform",
        deps=["the-numbers-weekly-box-office"],
        sql=f'''
            SELECT {_CHART_COLS_COMMON}
            FROM "the-numbers-weekly-box-office"
            WHERE title IS NOT NULL AND gross IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY chart_date, title ORDER BY total_gross DESC
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="the-numbers-annual-top-grossing-transform",
        deps=["the-numbers-annual-top-grossing"],
        sql='''
            SELECT
                CAST(year AS INTEGER)      AS year,
                CAST(rank AS INTEGER)      AS rank,
                title,
                release_date,
                distributor,
                genre,
                CAST(gross AS BIGINT)      AS gross,
                CAST(tickets_sold AS BIGINT) AS tickets_sold
            FROM "the-numbers-annual-top-grossing"
            WHERE title IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY year, title ORDER BY gross DESC
            ) = 1
        ''',
    ),
]
