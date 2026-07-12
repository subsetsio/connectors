"""World Prison Brief.

The site is a public Drupal app with no machine-readable API. Raw downloads
therefore scrape static region and country pages into stable parquet tables.
Each run is a full snapshot; country information is updated monthly according
to the WPB About page.
"""

import html
import re
from urllib.parse import urljoin

import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet

SLUG = "world-prison-brief"
BASE = "https://www.prisonstudies.org"
REGION_PATHS = [
    "/region/africa",
    "/region/asia",
    "/region/caribbean",
    "/region/northern-america",
    "/region/central-america",
    "/region/south-america",
    "/region/europe",
    "/region/middle-east",
    "/region/oceania",
]


def _fetch_text(path_or_url: str) -> str:
    url = path_or_url if path_or_url.startswith("http") else urljoin(BASE, path_or_url)
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _clean_text(raw: str) -> str | None:
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    text = html.unescape(raw).replace("\xa0", " ")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    text = " | ".join(line for line in lines if line)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def _slug_from_path(path: str) -> str:
    return path.rstrip("/").rsplit("/", 1)[-1]


def _country_title(page: str) -> str | None:
    match = re.search(r'<h1 class="title[^"]*".*?</h1>', page, re.S)
    return _clean_text(match.group(0)) if match else None


def _country_region(page: str) -> str | None:
    match = re.search(r'<span class="region-name.*?</span>', page, re.S)
    return _clean_text(match.group(0)) if match else None


def _country_links() -> list[dict]:
    seen = {}
    for region_path in REGION_PATHS:
        region_page = _fetch_text(region_path)
        region_name = region_path.rsplit("/", 1)[-1].replace("-", " ").title()
        for href, label in re.findall(
            r'<a href="(/country/[^"]+)"[^>]*>(.*?)</a>',
            region_page,
            re.S,
        ):
            slug = _slug_from_path(href)
            seen[slug] = {
                "jurisdiction_id": slug,
                "name": _clean_text(label),
                "region": region_name,
                "country_path": href,
                "country_url": urljoin(BASE, href),
            }
    return sorted(seen.values(), key=lambda row: row["jurisdiction_id"])


def _country_pages() -> list[tuple[dict, str]]:
    pages = []
    for row in _country_links():
        page = _fetch_text(row["country_path"])
        row = dict(row)
        row["name"] = _country_title(page) or row["name"]
        row["region"] = _country_region(page) or row["region"]
        pages.append((row, page))
    return pages


def _parse_current_stats(row: dict, page: str) -> list[dict]:
    match = re.search(
        r"<h2[^>]*>\s*Prison population data\s*</h2>.*?"
        r'(<table class="data d-table">.*?</table>)',
        page,
        re.S,
    )
    if not match:
        return []
    out = []
    for tr in re.findall(r"(?s)<tr[^>]*>(.*?)</tr>", match.group(1)):
        th = re.search(r"(?s)<th[^>]*>(.*?)</th>", tr)
        td = re.search(r"(?s)<td[^>]*>(.*?)</td>", tr)
        if not th or not td:
            continue
        value_html = td.group(1)
        comment = None
        comment_match = re.search(r'(?s)<div class="comment">(.*?)</div>', value_html)
        if comment_match:
            comment = _clean_text(comment_match.group(1))
            value_html = value_html[: comment_match.start()]
        out.append({
            "jurisdiction_id": row["jurisdiction_id"],
            "jurisdiction_name": row["name"],
            "region": row["region"],
            "indicator": _clean_text(th.group(1)),
            "value_text": _clean_text(value_html),
            "note": comment,
            "country_url": row["country_url"],
        })
    return out


def _parse_overview_trend(row: dict, page: str) -> list[dict]:
    match = re.search(
        r'(<table class="table table-striped views-table views-view-table cols-3">.*?</table>)',
        page,
        re.S,
    )
    if not match:
        return []
    rows = []
    for tr in re.findall(r"(?s)<tr[^>]*>(.*?)</tr>", match.group(1)):
        cells = re.findall(r"(?s)<td[^>]*>(.*?)</td>", tr)
        if len(cells) < 3:
            continue
        date_match = re.search(r'datetime="([^"]+)"', cells[0])
        rows.append({
            "jurisdiction_id": row["jurisdiction_id"],
            "jurisdiction_name": row["name"],
            "region": row["region"],
            "observation_date": date_match.group(1)[:10] if date_match else None,
            "year_text": _clean_text(cells[0]),
            "prison_population_total_text": _clean_text(cells[1]),
            "prison_population_rate_text": _clean_text(cells[2]),
            "country_url": row["country_url"],
        })
    return rows


def _cell_lines(cell_html: str) -> list[str]:
    text = _clean_text(cell_html) or ""
    parts = [part.strip() for part in text.split("|") if part.strip()]
    return parts or ([text] if text else [])


def _parse_plain_table(table_html: str) -> tuple[list[str], list[list[str]]]:
    trs = re.findall(r"(?s)<tr[^>]*>(.*?)</tr>", table_html)
    if not trs:
        return [], []
    headers = [_clean_text(cell) or "" for cell in re.findall(r"(?s)<td[^>]*>(.*?)</td>", trs[0])]
    rows = []
    for tr in trs[1:]:
        cells = re.findall(r"(?s)<td[^>]*>(.*?)</td>", tr)
        split_cells = [_cell_lines(cell) for cell in cells]
        width = max((len(cell) for cell in split_cells), default=0)
        for idx in range(width):
            rows.append([cell[idx] if idx < len(cell) else None for cell in split_cells])
    return headers, rows


def _parse_additional_tables(row: dict, page: str) -> list[dict]:
    out = []
    for section in re.findall(r'(?s)<div class="field__item">\s*<h3.*?</div>', page):
        title_match = re.search(r"(?s)<h3[^>]*>(.*?)</h3>", section)
        table_match = re.search(r"(?s)(<table>.*?</table>)", section)
        if not title_match or not table_match:
            continue
        table_title = _clean_text(title_match.group(1))
        headers, records = _parse_plain_table(table_match.group(1))
        for record in records:
            values = {f"column_{idx + 1}": value for idx, value in enumerate(record)}
            out.append({
                "jurisdiction_id": row["jurisdiction_id"],
                "jurisdiction_name": row["name"],
                "region": row["region"],
                "table_title": table_title,
                "headers": " | ".join(headers),
                **values,
                "country_url": row["country_url"],
            })
    return out


def _parse_source_notes(row: dict, page: str) -> list[dict]:
    notes = []
    for stat in _parse_current_stats(row, page):
        if stat["note"]:
            notes.append({
                "jurisdiction_id": row["jurisdiction_id"],
                "jurisdiction_name": row["name"],
                "region": row["region"],
                "note_type": "current_statistic",
                "subject": stat["indicator"],
                "note_text": stat["note"],
                "country_url": row["country_url"],
            })
    for dt, dd in re.findall(
        r'(?s)<dt class="d-table-cell dlcell col-md-6">(.*?)</dt>\s*'
        r'<dd class="d-table-cell dlcell col-md-6">(.*?)</dd>',
        page,
    ):
        label = _clean_text(dt)
        value = _clean_text(dd)
        if label and value and label != "Country":
            notes.append({
                "jurisdiction_id": row["jurisdiction_id"],
                "jurisdiction_name": row["name"],
                "region": row["region"],
                "note_type": "jurisdiction_metadata",
                "subject": label,
                "note_text": value,
                "country_url": row["country_url"],
            })
    return notes


JURISDICTIONS_SCHEMA = pa.schema([
    ("jurisdiction_id", pa.string()),
    ("name", pa.string()),
    ("region", pa.string()),
    ("country_path", pa.string()),
    ("country_url", pa.string()),
])

CURRENT_SCHEMA = pa.schema([
    ("jurisdiction_id", pa.string()),
    ("jurisdiction_name", pa.string()),
    ("region", pa.string()),
    ("indicator", pa.string()),
    ("value_text", pa.string()),
    ("note", pa.string()),
    ("country_url", pa.string()),
])

POP_TREND_SCHEMA = pa.schema([
    ("jurisdiction_id", pa.string()),
    ("jurisdiction_name", pa.string()),
    ("region", pa.string()),
    ("observation_date", pa.string()),
    ("year_text", pa.string()),
    ("prison_population_total_text", pa.string()),
    ("prison_population_rate_text", pa.string()),
    ("country_url", pa.string()),
])

ADDITIONAL_SCHEMA = pa.schema([
    ("jurisdiction_id", pa.string()),
    ("jurisdiction_name", pa.string()),
    ("region", pa.string()),
    ("table_title", pa.string()),
    ("headers", pa.string()),
    ("column_1", pa.string()),
    ("column_2", pa.string()),
    ("column_3", pa.string()),
    ("column_4", pa.string()),
    ("column_5", pa.string()),
    ("country_url", pa.string()),
])

NOTES_SCHEMA = pa.schema([
    ("jurisdiction_id", pa.string()),
    ("jurisdiction_name", pa.string()),
    ("region", pa.string()),
    ("note_type", pa.string()),
    ("subject", pa.string()),
    ("note_text", pa.string()),
    ("country_url", pa.string()),
])


def fetch_jurisdictions(node_id: str) -> None:
    save_raw_parquet(pa.Table.from_pylist(_country_links(), schema=JURISDICTIONS_SCHEMA), node_id)


def fetch_current_prison_statistics(node_id: str) -> None:
    rows = []
    for country, page in _country_pages():
        rows.extend(_parse_current_stats(country, page))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=CURRENT_SCHEMA), node_id)


def fetch_prison_population_trends(node_id: str) -> None:
    rows = []
    for country, page in _country_pages():
        rows.extend(_parse_overview_trend(country, page))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=POP_TREND_SCHEMA), node_id)


def fetch_additional_trend_tables(node_id: str) -> None:
    rows = []
    for country, page in _country_pages():
        rows.extend(_parse_additional_tables(country, page))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=ADDITIONAL_SCHEMA), node_id)


def fetch_source_notes(node_id: str) -> None:
    rows = []
    for country, page in _country_pages():
        rows.extend(_parse_source_notes(country, page))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=NOTES_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-additional-trend-tables", fn=fetch_additional_trend_tables, kind="download"),
    NodeSpec(id=f"{SLUG}-current-prison-statistics", fn=fetch_current_prison_statistics, kind="download"),
    NodeSpec(id=f"{SLUG}-jurisdictions", fn=fetch_jurisdictions, kind="download"),
    NodeSpec(id=f"{SLUG}-prison-population-trends", fn=fetch_prison_population_trends, kind="download"),
    NodeSpec(id=f"{SLUG}-source-notes", fn=fetch_source_notes, kind="download"),
]
