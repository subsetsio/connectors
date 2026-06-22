"""W3Techs — web technology usage surveys (market-share / usage time series).

W3Techs publishes no machine-readable API for its aggregate statistics (the only
documented API is a paid, per-site, republish-forbidden technology-detection
lookup). The statistics live as static HTML tables, with a yearly trend page per
survey category. Two trend metrics exist, and which one a category exposes
depends on the category's nature:

  * `/history_overview/<cat>/ms/y`  -> "Market Share": for categories where a
    site uses exactly one technology (web server, OS, server-side language, TLD,
    server location, ...). Distribution sums to ~100% within the category.
  * `/history_overview/<cat>/all/y` -> "Usage": for categories where a site may
    use several technologies (JS libraries, social widgets, image formats,
    structured-data formats, ...). Percentages need not sum to 100%.

The two are largely mutually exclusive (a non-existent view returns HTTP 404),
though some categories expose both. We therefore fetch BOTH views for every
category and keep whichever exist, tagging each row with a `metric`
discriminator. Each view's table is a fixed grid: a header row of dates
(`YYYY<br>D Mon`, ~January 2015 -> the current daily snapshot) and one body row
per technology (`<th>name` + one `<td>pct%` per date).

Shape: stateless full re-pull. The whole corpus is ~40 small HTML pages and a
few thousand (category, technology, date, metric, percent) rows — re-scraping
every run and overwriting is trivially cheap and picks up W3Techs' daily
revisions for free, so there is no watermark/cursor/state. One download node
(`w3techs-values`) scrapes everything into a single long-format parquet; one SQL
transform publishes the `w3techs-values` Delta table.
"""
import time
from datetime import date

import pyarrow as pa
from lxml import html as lh

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import CATEGORIES

# ASCII-only User-Agent (httpx rejects non-ASCII header values). W3Techs'
# robots.txt blocks only ia_archiver/Scrapy/TikTokSpider/Bytespider; a generic
# identified agent and /technologies/ are not disallowed.
_USER_AGENT = "subsets.io-connector/1.0 (+https://subsets.io)"

# (url path segment, metric label) for the two trend views.
_VIEWS = (("ms/y", "market_share"), ("all/y", "usage"))

# Politeness pause between page fetches; W3Techs intermittently drops the socket
# under rapid sequential requests (no documented rate limit, no 429/Retry-After).
_DELAY_SECONDS = 1.0

_MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}

SCHEMA = pa.schema([
    ("category", pa.string()),
    ("category_name", pa.string()),
    ("technology", pa.string()),
    ("date", pa.date32()),
    ("metric", pa.string()),
    ("percent", pa.float64()),
])


@transient_retry(attempts=6, min_wait=2, max_wait=60)
def _fetch_view(slug: str, view: str):
    """Fetch one category/view trend page. Returns the HTML, or None if the view
    does not exist (HTTP 404 — that metric isn't published for this category).
    Transient drops (ConnectTimeout) and 429/5xx are retried by the decorator;
    a genuine 404 returns cleanly and is NOT retried."""
    url = f"https://w3techs.com/technologies/history_overview/{slug}/{view}"
    resp = get(url, timeout=(30.0, 120.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.text


def _parse_header_dates(header_row) -> list:
    """Header is one empty leading cell then date cells, each rendered as
    `<td>YYYY<br>D Mon</td>` (e.g. 2015 / "1 Jan", 2026 / "21 Jun"). Returns one
    datetime.date per data column."""
    cells = header_row.xpath("./td | ./th")[1:]  # drop leading empty corner cell
    dates = []
    for c in cells:
        parts = [t.strip() for t in c.itertext() if t.strip()]
        year = int(parts[0])
        day_str, mon_str = parts[1].split()
        dates.append(date(year, _MONTHS[mon_str], int(day_str)))
    return dates


def _parse_percent(text: str):
    """'60.7%' -> 60.7, '<0.1%' -> 0.1 (upper bound), '' / 'n/a' -> None."""
    s = text.strip().replace("%", "").replace("<", "").replace(",", "")
    if not s or s.lower() in ("n/a", "na", "-", "?"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _pick_data_table(doc):
    """Of the page's tables, the data grid is the one whose first row carries the
    date columns and whose body rows each start with a <th> technology name plus
    one <td> per date."""
    for t in doc.xpath("//table"):
        rows = t.xpath("./tr") or t.xpath("./tbody/tr")
        if not rows:
            continue
        header_cells = rows[0].xpath("./td | ./th")
        data_rows = [r for r in rows if r.xpath("./th") and r.xpath("./td")]
        if len(data_rows) >= 1 and len(header_cells) >= 4:
            return rows[0], data_rows
    return None, None


def _parse_view(slug: str, name: str, view: str, metric: str) -> list:
    html_text = _fetch_view(slug, view)
    if html_text is None:
        return []  # this metric isn't published for this category
    header_row, data_rows = _pick_data_table(lh.fromstring(html_text))
    if header_row is None:
        raise AssertionError(f"{slug}/{view}: no data table found (layout changed?)")
    dates = _parse_header_dates(header_row)
    rows = []
    for r in data_rows:
        technology = r.xpath("./th")[0].text_content().strip()
        if not technology:
            continue
        cells = r.xpath("./td")
        if len(cells) != len(dates):
            raise AssertionError(
                f"{slug}/{view}/{technology}: {len(cells)} value cells vs {len(dates)} date columns"
            )
        for d, cell in zip(dates, cells):
            pct = _parse_percent(cell.text_content())
            if pct is None:
                continue
            rows.append({
                "category": slug,
                "category_name": name,
                "technology": technology,
                "date": d,
                "metric": metric,
                "percent": pct,
            })
    return rows


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    configure_http(headers={"User-Agent": _USER_AGENT})
    rows = []
    for slug, name in CATEGORIES.items():
        before = len(rows)
        for view, metric in _VIEWS:
            rows.extend(_parse_view(slug, name, view, metric))
            time.sleep(_DELAY_SECONDS)
        if len(rows) == before:
            # Every category must expose at least one trend view; zero rows means
            # both views 404'd or parsed empty — fail loudly rather than silently
            # shipping a partial corpus.
            raise AssertionError(f"{slug}: no rows from either trend view")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="w3techs-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="w3techs-values-transform",
        deps=["w3techs-values"],
        sql='''
            SELECT
                category,
                category_name,
                technology,
                CAST(date AS DATE)        AS date,
                metric,
                CAST(percent AS DOUBLE)   AS percent
            FROM "w3techs-values"
            WHERE percent IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY category, technology, date, metric
                ORDER BY percent DESC
            ) = 1
        ''',
    ),
]
