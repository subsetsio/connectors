"""Ministry of Education (China) — moe.gov.cn education statistics.

The source has no API/bulk export; the only surface is static HTML statistical
tables (research mechanism `scrape_html_tables`). Each rank-accepted entity is one
distinct national statistical table TYPE (identified by its Chinese title) that the
MoE republishes every year. One download spec per entity walks the year index
(1997-2024), and for each year finds that table's article on the year's national
('全国基本情况') index and parses its Excel-styled HTML <table> into a tidy long
form. The whole corpus is small and is re-pulled in full each run (stateless) —
the source publishes annually with no incremental query support, so there is no
watermark to keep.

Transport note: the site serves over plain HTTP and 302-redirects HTTPS->HTTP,
which breaks HTTPS-forcing clients; we therefore address it over http:// directly
(verified working). Pages are UTF-8.
"""

import logging
import re

import lxml.html
import pyarrow as pa

from constants import ENTITY_IDS, ENTITY_TITLES
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

log = logging.getLogger("ministry-of-education")

SLUG = "ministry-of-education"
# Year-index page: any recent year page lists every year's landing URL (1997-2024).
# http:// is required here — the site 302-redirects https->http (see module docstring).
YEAR_INDEX_URL = "http://www.moe.gov.cn/jyb_sjzl/moe_560/2024/"
MAX_INDEX_PAGES = 30  # safety ceiling for quanguo index pagination

SCHEMA = pa.schema([
    ("entity_id", pa.string()),
    ("year", pa.int32()),
    ("tbl_idx", pa.int16()),
    ("row_idx", pa.int32()),
    ("col_idx", pa.int32()),
    ("row_label", pa.string()),
    ("col_label", pa.string()),
    ("value", pa.float64()),
])

_NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
_ARTICLE_RE = re.compile(r"/t\d{8}_\d+\.html$")
_YEAR_LABEL_RE = re.compile(r"^((?:19|20)\d{2})年教育统计数据$")


@transient_retry()  # 6 attempts, exponential backoff on 429/5xx/network errors
def _fetch(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return resp.text


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").replace("\xa0", " ")).strip()


def _is_num(s: str) -> bool:
    s = s.replace(",", "").replace(" ", "")
    return bool(_NUM_RE.match(s)) and bool(re.search(r"\d", s))


def _grid_from_table(tbl) -> list[list[str]]:
    """Expand rowspan/colspan into a dense matrix of cell texts."""
    trs = tbl.xpath(".//tr")
    occupied: dict[tuple[int, int], str] = {}
    for r, tr in enumerate(trs):
        c = 0
        for cell in tr.xpath("./td|./th"):
            while (r, c) in occupied:
                c += 1
            txt = _clean(cell.text_content())
            try:
                rs = max(1, int(cell.get("rowspan", 1)))
            except (TypeError, ValueError):
                rs = 1
            try:
                cs = max(1, int(cell.get("colspan", 1)))
            except (TypeError, ValueError):
                cs = 1
            for dr in range(rs):
                for dc in range(cs):
                    occupied[(r + dr, c + dc)] = txt
            c += cs
    nrows = len(trs)
    ncols = max((cc for (_, cc) in occupied), default=-1) + 1
    mat = [["" for _ in range(ncols)] for _ in range(nrows)]
    for (rr, cc), t in occupied.items():
        if rr < nrows and cc < ncols:
            mat[rr][cc] = t
    return mat


def _melt(mat: list[list[str]]) -> list[tuple[int, int, str, str, float]]:
    """Cross-tab -> (row_idx, col_idx, row_label, col_label, value) records.

    Header rows = leading rows with no numeric cell. Label cols = leading cols
    with no numeric cell in the body. Body numeric cells become long-form values.
    """
    if not mat or not mat[0]:
        return []
    nrows, ncols = len(mat), len(mat[0])
    H = 0
    for row in mat:
        if any(_is_num(x) for x in row):
            break
        H += 1
    if H == 0 or H >= nrows:
        return []
    L = 0
    for c in range(ncols):
        if any(_is_num(mat[r][c]) for r in range(H, nrows)):
            break
        L += 1
    L = max(L, 1)
    out: list[tuple[int, int, str, str, float]] = []
    for r in range(H, nrows):
        row_label = " / ".join(x for x in (mat[r][c] for c in range(L)) if x)
        for c in range(L, ncols):
            val = mat[r][c]
            if not _is_num(val):
                continue
            # dedupe header fragments while preserving order (merged unit rows repeat)
            col_label = " / ".join(
                dict.fromkeys(x for x in (mat[h][c] for h in range(H)) if x)
            )
            out.append((r, c, row_label, col_label, float(val.replace(",", ""))))
    return out


def _parse_article(html: str) -> list[tuple[int, int, int, str, str, float]]:
    """Parse all leaf data tables in an article -> (tbl_idx,row,col,rl,cl,value)."""
    doc = lxml.html.fromstring(html)
    for bad in doc.xpath("//style|//script"):
        bad.getparent().remove(bad)
    leaves = [t for t in doc.xpath("//table") if not t.xpath(".//table")]
    recs: list[tuple[int, int, int, str, str, float]] = []
    for ti, tbl in enumerate(leaves):
        mat = _grid_from_table(tbl)
        if sum(_is_num(x) for row in mat for x in row) < 3:
            continue
        for (ri, ci, rl, cl, v) in _melt(mat):
            recs.append((ti, ri, ci, rl, cl, v))
    return recs


def _discover_years() -> dict[int, str]:
    """Map statistical year -> that year's landing URL, from the year index."""
    doc = lxml.html.fromstring(_fetch(YEAR_INDEX_URL))
    doc.make_links_absolute(YEAR_INDEX_URL)
    years: dict[int, str] = {}
    for a in doc.xpath("//a[@href]"):
        m = _YEAR_LABEL_RE.match((a.text_content() or "").strip())
        if m:
            years.setdefault(int(m.group(1)), a.get("href"))
    return years


def _find_quanguo_index(landing_url: str) -> str | None:
    """From a year landing page, find its national ('全国基本情况') index URL."""
    doc = lxml.html.fromstring(_fetch(landing_url))
    doc.make_links_absolute(landing_url)
    for a in doc.xpath("//a[@href]"):
        href = a.get("href")
        txt = (a.text_content() or "").strip()
        if "全国基本情况" in txt or "quanguo" in href or "_qg/" in href:
            return href
    return None


def _find_article(quanguo_url: str, title: str) -> str | None:
    """Paginate a national index (index.html, index_1.html, ...) for `title`."""
    base = quanguo_url if quanguo_url.endswith("/") else quanguo_url.rsplit("/", 1)[0] + "/"
    for n in range(MAX_INDEX_PAGES):
        page = base if n == 0 else f"{base}index_{n}.html"
        try:
            html = _fetch(page)
        except Exception as e:  # noqa: BLE001 - a 404 just means past the last page
            if "404" in str(e):
                return None
            log.warning("index fetch failed %s: %s", page, e.__class__.__name__)
            return None
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(page)
        found_links = False
        for a in doc.xpath("//a[@href]"):
            href = a.get("href")
            if not _ARTICLE_RE.search(href):
                continue
            found_links = True
            label = (a.get("title") or a.text_content() or "").strip()
            if label == title:
                return href
        if not found_links:
            return None  # no article links on this page -> past the last page
    raise RuntimeError(f"quanguo index exceeded {MAX_INDEX_PAGES} pages: {base}")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime hands us the spec id; it IS the asset name
    entity_id = node_id[len(SLUG) + 1:]  # strip "ministry-of-education-"
    title = ENTITY_TITLES[entity_id]

    years = _discover_years()
    rows: list[dict] = []
    matched_years = 0
    for year in sorted(years):
        landing = years[year]
        try:
            quanguo = _find_quanguo_index(landing)
            if not quanguo:
                continue  # older years use a structure without a national index
            article = _find_article(quanguo, title)
            if not article:
                continue  # this table not published (under this title) that year
            recs = _parse_article(_fetch(article))
            if not recs:
                continue
            matched_years += 1
            for (ti, ri, ci, rl, cl, v) in recs:
                rows.append({
                    "entity_id": entity_id,
                    "year": year,
                    "tbl_idx": ti,
                    "row_idx": ri,
                    "col_idx": ci,
                    "row_label": rl,
                    "col_label": cl,
                    "value": v,
                })
        except Exception as e:  # noqa: BLE001 - one bad year must not sink the entity
            log.warning("%s year %s failed: %s: %s", entity_id, year, e.__class__.__name__, e)
            continue

    if not rows:
        raise RuntimeError(f"{entity_id} ({title!r}): no data parsed across any year")
    log.info("%s: %d rows across %d years", entity_id, len(rows), matched_years)
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT DISTINCT
                CAST(year AS INTEGER)    AS year,
                CAST(tbl_idx AS INTEGER) AS table_index,
                CAST(row_idx AS INTEGER) AS row_index,
                CAST(col_idx AS INTEGER) AS col_index,
                row_label,
                col_label,
                CAST(value AS DOUBLE)    AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL AND row_label IS NOT NULL AND row_label <> ''
        ''',
    )
    for s in DOWNLOAD_SPECS
]
