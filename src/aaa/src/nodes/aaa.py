"""AAA Daily Fuel Gauge Report (gasprices.aaa.com) connector.

Source has no developer API: the WordPress theme server-renders all fuel-price
data into static HTML tables (mechanism `scrape_html`). Three published subsets,
split by geographic level because each has a different key-column list:

  * aaa-national-fuel-prices  - U.S. national average (root page)
  * aaa-state-fuel-prices     - per state/territory statewide average
  * aaa-metro-fuel-prices     - per metropolitan area within each state

Each page is a daily SNAPSHOT: it shows the current average plus Yesterday /
Week Ago / Month Ago / Year Ago lookbacks, but no real history. We therefore
keep only the "Current Avg." row, stamped with the page's stated "as of" date,
and write it as a date-keyed raw batch (`<spec-id>-<YYYY-MM-DD>`). Closed
batches are immutable; daily runs accumulate them and each transform glob-unions
`<spec-id>-*` into a growing time series. Re-running on the same day overwrites
that day's batch (idempotent).

This is a stateless full re-pull every run (no watermark/cursor): the corpus is
~53 small HTML pages, cheap to refetch, and revisions are picked up for free.
robots.txt requests Crawl-delay: 10 (advisory); we space requests modestly and
let transient_retry absorb Cloudflare 429/503. State codes are discovered from
the root page's state <select>, not hardcoded.
"""

import re
import time
from datetime import date, datetime, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec, SqlNodeSpec,
    get, configure_http, transient_retry,
    save_raw_parquet,
)

ROOT = "https://gasprices.aaa.com/"
# ASCII-only User-Agent (httpx headers must be ASCII): a real browser UA gets
# clean 200s past Cloudflare; the default UA risks a challenge page.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
REQUEST_SPACING_S = 1.5  # polite gap between per-state page fetches

# Canonical fuel-grade labels, keyed by the header text the tables use.
GRADE_MAP = {"regular": "Regular", "mid-grade": "Mid-Grade", "mid": "Mid-Grade",
             "premium": "Premium", "diesel": "Diesel", "e85": "E85"}

NATIONAL_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("fuel_grade", pa.string()),
    ("price_usd", pa.float64()),
])
STATE_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("state_code", pa.string()),
    ("fuel_grade", pa.string()),
    ("price_usd", pa.float64()),
])
METRO_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("state_code", pa.string()),
    ("metro_area", pa.string()),
    ("fuel_grade", pa.string()),
    ("price_usd", pa.float64()),
])


@transient_retry()
def _fetch(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _strip(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ").strip()


def _as_of(html: str) -> date:
    """The page's stated observation date ('as of M/D/YY'); UTC today if absent."""
    m = re.search(r"as of\s+(\d{1,2})/(\d{1,2})/(\d{2,4})", html)
    if not m:
        return datetime.now(timezone.utc).date()
    mo, da, yr = (int(x) for x in m.groups())
    if yr < 100:
        yr += 2000
    return date(yr, mo, da)


def _price(cell: str):
    t = _strip(cell).replace("$", "").replace(",", "")
    try:
        return float(t)
    except ValueError:
        return None  # missing grade or '-' placeholder


def _current_avg(table_html: str) -> dict:
    """Parse a 'table-mob' price table -> {canonical_grade: price} for the
    'Current Avg.' row. Grades are read from the header (E85 etc. may be absent)."""
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, re.S)
    if not rows:
        return {}
    header = [_strip(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", rows[0], re.S)]
    grades = [GRADE_MAP.get(g.lower()) for g in header[1:]]
    for r in rows[1:]:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)
        if not cells or not _strip(cells[0]).lower().startswith("current"):
            continue
        out = {}
        for g, c in zip(grades, cells[1:]):
            p = _price(c)
            if g and p is not None:
                out[g] = p
        return out
    return {}


def _table_spans(html: str):
    """(start_offset, inner_html) for every table-mob, in document order."""
    return [(m.start(), m.group(1))
            for m in re.finditer(r'<table class="table-mob">(.*?)</table>', html, re.S)]


def _state_codes(html: str) -> list:
    codes = set()
    for val in re.findall(r'<option[^>]*\bvalue="([^"]*)"', html, re.I):
        v = val.strip().upper()
        if len(v) == 2 and v.isalpha() and v != "US":
            codes.add(v)
    return sorted(codes)


def _batch_id(node_id: str, observed: date) -> str:
    return f"{node_id}-{observed.isoformat()}"


# ---- download nodes ---------------------------------------------------------

def fetch_national(node_id: str) -> None:
    configure_http(headers={"User-Agent": UA})
    html = _fetch(ROOT)
    observed = _as_of(html)
    tables = _table_spans(html)
    if not tables:
        raise AssertionError("national page has no table-mob; markup changed")
    prices = _current_avg(tables[0][1])
    if not prices:
        raise AssertionError("national 'Current Avg.' row not found")
    rows = [{"date": observed, "fuel_grade": g, "price_usd": p}
            for g, p in sorted(prices.items())]
    table = pa.Table.from_pylist(rows, schema=NATIONAL_SCHEMA)
    save_raw_parquet(table, _batch_id(node_id, observed))


def fetch_state(node_id: str) -> None:
    configure_http(headers={"User-Agent": UA})
    root_html = _fetch(ROOT)
    observed = _as_of(root_html)
    codes = _state_codes(root_html)
    if len(codes) < 50:
        raise AssertionError(f"only {len(codes)} state codes discovered: {codes}")
    rows = []
    for i, code in enumerate(codes):
        if i:
            time.sleep(REQUEST_SPACING_S)
        try:
            html = _fetch(f"{ROOT}?state={code}")
        except Exception as e:  # one bad state page must not sink the whole spec
            print(f"[aaa] state {code} fetch failed: {type(e).__name__}: {e}")
            continue
        tables = _table_spans(html)
        if not tables:
            print(f"[aaa] state {code}: no price table found, skipping")
            continue
        for g, p in _current_avg(tables[0][1]).items():
            rows.append({"date": observed, "state_code": code,
                         "fuel_grade": g, "price_usd": p})
    if not rows:
        raise AssertionError("no state prices parsed across any state page")
    table = pa.Table.from_pylist(rows, schema=STATE_SCHEMA)
    save_raw_parquet(table, _batch_id(node_id, observed))


def fetch_metro(node_id: str) -> None:
    configure_http(headers={"User-Agent": UA})
    root_html = _fetch(ROOT)
    observed = _as_of(root_html)
    codes = _state_codes(root_html)
    if len(codes) < 50:
        raise AssertionError(f"only {len(codes)} state codes discovered: {codes}")
    rows = []
    for i, code in enumerate(codes):
        if i:
            time.sleep(REQUEST_SPACING_S)
        try:
            html = _fetch(f"{ROOT}?state={code}")
        except Exception as e:
            print(f"[aaa] state {code} fetch failed: {type(e).__name__}: {e}")
            continue
        spans = _table_spans(html)  # [0] is statewide; metros follow each <h3 data-title>
        # pair each metro heading with the first price table after it
        heads = [(m.start(), _strip(m.group(1)))
                 for m in re.finditer(r'<h3[^>]*data-title[^>]*>(.*?)</h3>', html, re.S)]
        for pos, name in heads:
            tbl = next((t for (s, t) in spans if s > pos), None)
            if tbl is None or not name:
                continue
            for g, p in _current_avg(tbl).items():
                rows.append({"date": observed, "state_code": code, "metro_area": name,
                             "fuel_grade": g, "price_usd": p})
    if not rows:
        raise AssertionError("no metro prices parsed across any state page")
    table = pa.Table.from_pylist(rows, schema=METRO_SCHEMA)
    save_raw_parquet(table, _batch_id(node_id, observed))


DOWNLOAD_SPECS = [
    NodeSpec(id="aaa-national-fuel-prices", fn=fetch_national, kind="download"),
    NodeSpec(id="aaa-state-fuel-prices", fn=fetch_state, kind="download"),
    NodeSpec(id="aaa-metro-fuel-prices", fn=fetch_metro, kind="download"),
]


# ---- transform nodes (one published Delta table per subset) -----------------

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="aaa-national-fuel-prices-transform",
        deps=["aaa-national-fuel-prices"],
        key=("date", "fuel_grade"),
        temporal="date",
        sql='''
            SELECT DISTINCT
                CAST(date AS DATE)        AS date,
                fuel_grade,
                CAST(price_usd AS DOUBLE) AS price_usd
            FROM "aaa-national-fuel-prices"
            WHERE price_usd > 0
        ''',
    ),
    SqlNodeSpec(
        id="aaa-state-fuel-prices-transform",
        deps=["aaa-state-fuel-prices"],
        key=("date", "state_code", "fuel_grade"),
        temporal="date",
        sql='''
            SELECT DISTINCT
                CAST(date AS DATE)        AS date,
                state_code,
                fuel_grade,
                CAST(price_usd AS DOUBLE) AS price_usd
            FROM "aaa-state-fuel-prices"
            WHERE price_usd > 0
        ''',
    ),
    SqlNodeSpec(
        id="aaa-metro-fuel-prices-transform",
        deps=["aaa-metro-fuel-prices"],
        key=("date", "state_code", "metro_area", "fuel_grade"),
        temporal="date",
        sql='''
            SELECT DISTINCT
                CAST(date AS DATE)        AS date,
                state_code,
                metro_area,
                fuel_grade,
                CAST(price_usd AS DOUBLE) AS price_usd
            FROM "aaa-metro-fuel-prices"
            WHERE price_usd > 0
        ''',
    ),
]
