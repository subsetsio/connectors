"""GACC (General Administration of Customs of China) — monthly trade statistics.

Mechanism (per research): static-HTML scrape of the English site's monthly
statistical reports. There is no usable structured API — the richer query
platform at stats.customs.gov.cn sits behind a $_ts obfuscated-JS anti-bot wall
(HTTP 412) and cannot be reached server-side.

Discovery is a two-hop crawl:
  1. stable per-year index pages
     http://english.customs.gov.cn/statics/report/monthly{YEAR}.html
     (and monthly.html for the current year). Each is one <table> whose 19 rows
     are the standardized report TYPES and whose 12 columns are the months;
     each populated cell links to a /Statics/<uuid>.html data page.
  2. each data page is one <table> of real values for that (report type, month).
The /Statics/<uuid>.html URLs are random and change every month, so they are
never reconstructed — always rediscovered by crawling the (stable) index pages.

Fetch shape: stateless full re-pull. The whole corpus is small (~19 report
types x ~9 years x ~12 months of small HTML tables) and the source publishes
revised figures, so re-crawling everything each run and overwriting is correct
and simplest. There is no incremental query parameter on this surface.

Each report type has its own table layout (by country / by HS section / by
customs regime / by commodity / summary time series). Rather than 19 bespoke
schemas, every data table is melted to one uniform LONG format
(report_type, page_year, page_month, row_label, col_index, col_header, unit,
value_text, value); the per-subset SQL transform is then a thin parse-and-type
pass over that shared shape.
"""

import re
import html

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
)
from constants import ENTITY_IDS

BASE = "http://english.customs.gov.cn"
_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
_PERIODCODE = re.compile(r"\d+(to\d+)?$")

RAW_SCHEMA = pa.schema([
    ("report_type", pa.string()),
    ("page_year", pa.int32()),
    ("page_month", pa.int32()),
    ("row_index", pa.int32()),
    ("row_label", pa.string()),
    ("col_index", pa.int32()),
    ("col_header", pa.string()),
    ("unit", pa.string()),
    ("value_text", pa.string()),
    ("value", pa.float64()),
])


# ---- HTML helpers -----------------------------------------------------------

@transient_retry()
def _http_get(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def _slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def _parse_value(s: str):
    t = s.replace(",", "").replace("%", "").strip()
    if t in ("", "-", "--", "—"):
        return None
    try:
        return float(t)
    except ValueError:
        return None


def _real_number(s: str) -> bool:
    """A genuine magnitude/percentage cell, NOT a bare period code ('1', '1to3')."""
    t = s.strip()
    if _PERIODCODE.fullmatch(t):
        return False
    return _parse_value(t) is not None


def _scope(tok: str) -> str:
    if re.fullmatch(r"\d+", tok):
        return "current"
    if re.fullmatch(r"\d+to\d+", tok):
        return "cumulative"
    return tok


def _parse_grid(table_html: str) -> list:
    """Expand an HTML table (with colspan/rowspan) into a dense list-of-lists grid."""
    grid, occ = [], {}
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", table_html, re.S):
        cells = re.findall(r"<t[dh]([^>]*)>(.*?)</t[dh]>", row, re.S)
        out, ci = [], 0

        def _pending():
            nonlocal ci
            while ci in occ and occ[ci][1] > 0:
                txt, rem = occ[ci]
                out.append(txt)
                occ[ci] = (txt, rem - 1)
                ci += 1

        for attrs, inner in cells:
            _pending()
            m = re.search(r'colspan="?(\d+)', attrs)
            cs = int(m.group(1)) if m else 1
            m = re.search(r'rowspan="?(\d+)', attrs)
            rs = int(m.group(1)) if m else 1
            text = _clean(inner)
            for _ in range(cs):
                out.append(text)
                if rs > 1:
                    occ[ci] = (text, rs - 1)
                ci += 1
        _pending()
        grid.append(out)
    return grid


def _melt(grid: list) -> list:
    """Melt one report table's grid into long-format cell records."""
    if not grid:
        return []

    unit = None
    for row in grid:
        for c in row:
            if c.lower().startswith("unit"):
                unit = (c.split(":", 1)[-1].strip() if ":" in c else c) or None
                break
        if unit:
            break

    def is_data(row):
        return bool(row) and bool(row[0]) and any(_real_number(c) for c in row[1:])

    first = next((i for i, r in enumerate(grid) if is_data(r)), None)
    if first is None:
        return []

    def nonempty_same(r):
        ne = [c for c in r if c]
        return len(ne) > 0 and len(set(ne)) <= 1

    def is_unit_row(r):
        return any(c.lower().startswith("unit") for c in r)

    # Header block = leading rows before first data row, minus the spanned title
    # row and the unit caption. Includes the period-scope row ('1'/'1to1').
    hdr = [r for r in grid[:first] if not nonempty_same(r) and not is_unit_row(r)]

    def col_header(ci):
        parts = []
        for r in hdr:
            if ci < len(r) and r[ci]:
                tok = _scope(r[ci]) if _PERIODCODE.fullmatch(r[ci]) else r[ci]
                if tok and tok not in parts:
                    parts.append(tok)
        return " / ".join(parts) or None

    out = []
    for ri, row in enumerate(grid[first:]):
        label = row[0] if row else ""
        if not label or label.lower().startswith("unit") or nonempty_same(row):
            continue
        for ci in range(1, len(row)):
            out.append({
                "row_index": ri,
                "row_label": label,
                "col_index": ci,
                "col_header": col_header(ci),
                "unit": unit,
                "value_text": row[ci],
                "value": _parse_value(row[ci]),
            })
    return out


def _largest_table(page: str):
    tables = re.findall(r"<table.*?</table>", page, re.S)
    return max(tables, key=len) if tables else None


# ---- crawl ------------------------------------------------------------------

def _discover_years() -> list:
    page = _http_get(f"{BASE}/statics/report/monthly.html").text
    sel = re.search(r'<select id="monthlysel".*?</select>', page, re.S)
    years = sorted({int(y) for y in re.findall(r'<option value="(\d{4})"', sel.group(0))}) if sel else []
    if not years:
        raise AssertionError("monthly index: no year options found in #monthlysel")
    return years


def _index_page(year: int) -> str:
    """Per-year index HTML. The current year lives at monthly.html (its
    monthly{year}.html does not exist and 404s); past years have monthly{year}.html."""
    r = get(f"{BASE}/statics/report/monthly{year}.html", timeout=(10.0, 120.0))
    if r.status_code == 200 and "monthlysel" in r.text:
        return r.text
    return _http_get(f"{BASE}/statics/report/monthly.html").text


def _row_month_links(index_html: str, entity_slug: str) -> list:
    """In one year's index table, find the row whose title slug matches the
    entity and return its [(month_int, data_url), ...]."""
    for row in re.findall(r"<tr>(.*?)</tr>", index_html, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
        if not tds:
            continue
        title = _clean(tds[0])
        if not title or _slug(title) != entity_slug:
            continue
        links = []
        for url, text in re.findall(r"<a[^>]*href=([^ >\"']+)[^>]*>(.*?)</a>", row, re.S):
            mn = _MONTHS.get(_clean(text)[:3].lower())
            if mn:
                links.append((mn, html.unescape(url.strip())))
        return links
    return []


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("gacc-"):]

    rows = []
    for year in _discover_years():
        index_html = _index_page(year)
        for month, url in _row_month_links(index_html, entity):
            page = _http_get(url).text
            table = _largest_table(page)
            if not table:
                continue
            for rec in _melt(_parse_grid(table)):
                rec["report_type"] = entity
                rec["page_year"] = year
                rec["page_month"] = month
                rows.append(rec)

    if not rows:
        raise AssertionError(f"{asset}: crawl produced zero rows (report type vanished?)")

    table = pa.Table.from_pylist(
        [{k: r.get(k) for k in RAW_SCHEMA.names} for r in rows],
        schema=RAW_SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"gacc-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# ---- transforms: one thin SQL pass per subset -------------------------------
# The two Summary tables (report type 1) are already a time series: each monthly
# page repeats the full history (row_label = 'YYYY.MM'/'YYYY'), so dedup keeping
# the most recent page. Every other report type is a per-month cross-section
# (the period is the page year-month; row_label is a country/section/commodity).

def _is_summary(download_id: str) -> bool:
    return download_id.startswith("gacc-1-summary")


def _summary_sql(did: str) -> str:
    return f'''
        SELECT
            row_label                    AS period,
            col_index,
            col_header                   AS measure,
            unit,
            CAST(value AS DOUBLE)        AS value
        FROM "{did}"
        WHERE value IS NOT NULL
        QUALIFY row_number() OVER (
            PARTITION BY row_label, col_index
            ORDER BY page_year DESC, page_month DESC
        ) = 1
    '''


def _crosssection_sql(did: str) -> str:
    return f'''
        SELECT
            make_date(page_year, page_month, 1) AS period,
            page_year                           AS year,
            page_month                          AS month,
            row_label,
            col_index,
            col_header                          AS measure,
            unit,
            CAST(value AS DOUBLE)               AS value
        FROM "{did}"
        WHERE value IS NOT NULL
        QUALIFY row_number() OVER (
            PARTITION BY page_year, page_month, row_label, col_index
            ORDER BY value
        ) = 1
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_summary_sql(s.id) if _is_summary(s.id) else _crosssection_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
