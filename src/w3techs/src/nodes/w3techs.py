"""W3Techs — web technology usage surveys (market-share time series).

W3Techs publishes no machine-readable API for its aggregate market-share
statistics (the only documented API is a paid, per-site, republish-forbidden
technology-detection lookup). The statistics live as static HTML tables, one
"history_overview/.../ms/y" page per survey category, giving a yearly
market-share trend (~January 2015 -> the current snapshot) for each technology
within that category.

Shape: stateless full re-pull. The whole corpus is ~27 small HTML pages and a
few thousand (category, technology, date, percent) rows — re-scraping every run
and overwriting is trivially cheap and picks up W3Techs' daily revisions for
free, so there is no watermark/cursor/state. One download node
(`w3techs-values`) scrapes all categories into a single long-format parquet;
one SQL transform publishes the `w3techs-values` Delta table.
"""
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

_MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}

SCHEMA = pa.schema([
    ("category", pa.string()),
    ("category_name", pa.string()),
    ("technology", pa.string()),
    ("date", pa.date32()),
    ("market_share_percent", pa.float64()),
])


@transient_retry(attempts=6, min_wait=2, max_wait=60)
def _fetch_category(slug: str) -> str:
    """Fetch one category's yearly market-share trend page. Retries transient
    network/5xx/429 (W3Techs intermittently drops the socket mid-handshake)."""
    url = f"https://w3techs.com/technologies/history_overview/{slug}/ms/y"
    resp = get(url, timeout=(30.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _parse_header_dates(header_row) -> list:
    """The header row is one empty leading cell followed by date cells, each
    rendered as `<td>YYYY<br>D Mon</td>` (e.g. 2015 / "1 Jan", 2026 / "21 Jun").
    Returns a list of datetime.date, one per data column (header minus the
    leading empty cell)."""
    cells = header_row.xpath("./td | ./th")[1:]  # drop leading empty corner cell
    dates = []
    for c in cells:
        parts = [t.strip() for t in c.itertext() if t.strip()]
        # parts == ["2015", "1 Jan"]; be tolerant of extra whitespace nodes.
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
    """Of the page's tables, the data grid is the one whose first row carries
    the date columns and whose body rows each start with a <th> technology name
    plus one <td> per date."""
    for t in doc.xpath("//table"):
        rows = t.xpath("./tr") or t.xpath("./tbody/tr")
        if not rows:
            continue
        header_cells = rows[0].xpath("./td | ./th")
        data_rows = [r for r in rows if r.xpath("./th") and r.xpath("./td")]
        if len(data_rows) >= 2 and len(header_cells) >= 5:
            return rows[0], data_rows
    return None, None


def _parse_category(slug: str, name: str) -> list:
    doc = lh.fromstring(_fetch_category(slug))
    header_row, data_rows = _pick_data_table(doc)
    if header_row is None:
        # Layout changed; fail loudly rather than silently yield nothing.
        raise AssertionError(f"{slug}: no market-share data table found on page")
    dates = _parse_header_dates(header_row)
    rows = []
    for r in data_rows:
        technology = r.xpath("./th")[0].text_content().strip()
        if not technology:
            continue
        cells = r.xpath("./td")
        if len(cells) != len(dates):
            # Fixed grid is expected; a mismatch means alignment is ambiguous.
            raise AssertionError(
                f"{slug}/{technology}: {len(cells)} value cells but {len(dates)} date columns"
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
                "market_share_percent": pct,
            })
    return rows


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    configure_http(headers={"User-Agent": _USER_AGENT})
    rows = []
    for slug, name in CATEGORIES.items():
        rows.extend(_parse_category(slug, name))
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
                CAST(date AS DATE)                AS date,
                CAST(market_share_percent AS DOUBLE) AS market_share_percent
            FROM "w3techs-values"
            WHERE market_share_percent IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY category, technology, date
                ORDER BY market_share_percent DESC
            ) = 1
        ''',
    ),
]
