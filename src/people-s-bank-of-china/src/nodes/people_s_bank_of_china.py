"""People's Bank of China (PBOC) — Survey & Statistics Department.

PBOC has no JSON/REST API. It publishes a static HTML statistics portal under
/en/3688247/3688975/ (Data), organized by year -> category -> a `data_table`
listing one row per distinct statistical table. Each table is offered as parallel
.htm / .xls(x) / .pdf files at point-in-time URLs (the upload-timestamp id is not
reconstructable, so links must be harvested by scraping the category index pages).

Each statistical table is a bilingual (Chinese/English) Microsoft-Office-exported
grid. Two orientations occur:
  A) items in rows, periods (YYYY.MM) across a header row -- the common case,
     sometimes with a unit/measure sub-header row (e.g. "100million USD" vs
     "100million SDR", or "Stock" vs "Growth Rate(%)").
  B) transposed: periods down a column, items across the header (Corporate Goods
     Price Indices).
One yearly file carries a full year of monthly columns. We crawl every year the
portal exposes for the table's category, parse each file to long-format
(item, period, value), and publish one Delta table per entity:
period x item time series. Measure sub-labels are folded into `item`.

This connector covers the 22 clean monthly/periodic time-series tables. PBOC's
per-file cross-sectional matrix snapshots (Financial Accounts, the IMF reserves
template, the quarterly Assets-and-Liabilities snapshot) are a different shape and
were ranked below the publish threshold.
"""

import io
import re
import time

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson

SLUG = "people-s-bank-of-china"
BASE = "https://www.pbc.gov.cn"
LANDING = "/en/3688247/3688975/index.html"

# entity_id -> (category, exact table title) — copied from the collect catalog /
# rank-accepted entity union. Used to locate this table across the year index pages.
ENTITY_META = {
    'aggregate-financing-to-the-real-economy__aggregate-financing-to-the-real-economy-flow': ('Aggregate Financing to the Real Economy', 'Aggregate Financing to the Real Economy (Flow)'),
    'aggregate-financing-to-the-real-economy__aggregate-financing-to-the-real-economy-stock': ('Aggregate Financing to the Real Economy', 'Aggregate Financing to the Real Economy (Stock)'),
    'corporate-goods-price-indices__corporate-goods-price-indices-cgpi': ('Corporate Goods Price Indices', 'Corporate Goods Price Indices (CGPI)'),
    'financial-market-statistics__statistics-of-chinabond-government-securities-yield': ('Financial Market Statistics', 'Statistics of Chinabond Government Securities Yield'),
    'financial-market-statistics__statistics-of-domestic-debt-securities': ('Financial Market Statistics', 'Statistics of Domestic Debt Securities'),
    'financial-market-statistics__statistics-of-interbank-lending': ('Financial Market Statistics', 'Statistics of Interbank Lending'),
    'financial-market-statistics__statistics-of-interbank-pledged-repo': ('Financial Market Statistics', 'Statistics of Interbank Pledged Repo'),
    'financial-market-statistics__statistics-of-shibor': ('Financial Market Statistics', 'Statistics of Shibor'),
    'financial-market-statistics__statistics-of-stock-market': ('Financial Market Statistics', 'Statistics of Stock Market'),
    'money-and-banking-statistics__balance-sheet-of-monetary-authority': ('Money and Banking Statistics', 'Balance Sheet of Monetary Authority'),
    'money-and-banking-statistics__balance-sheet-of-other-depository-corporations': ('Money and Banking Statistics', 'Balance Sheet of Other Depository Corporations'),
    'money-and-banking-statistics__depository-corporations-survey': ('Money and Banking Statistics', 'Depository Corporations Survey'),
    'money-and-banking-statistics__domestic-rmb-financial-assets-held-by-overseas-entities': ('Money and Banking Statistics', 'Domestic RMB Financial Assets Held by Overseas Entities'),
    'money-and-banking-statistics__exchange-rate': ('Money and Banking Statistics', 'Exchange Rate'),
    'money-and-banking-statistics__money-supply': ('Money and Banking Statistics', 'Money Supply'),
    'money-and-banking-statistics__official-reserve-assets': ('Money and Banking Statistics', 'Official reserve assets'),
    'sources-and-uses-of-credit-funds-of-financial-institutions__sources-uses-of-credit-funds-of-depository-financial-institutions-in-foreign-currency': ('Sources and Uses of Credit Funds of Financial Institutions', 'Sources & Uses of Credit Funds of Depository Financial Institutions (in Foreign Currency)'),
    'sources-and-uses-of-credit-funds-of-financial-institutions__sources-uses-of-credit-funds-of-depository-financial-institutions-in-rmb-and-foreign-currency': ('Sources and Uses of Credit Funds of Financial Institutions', 'Sources & Uses of Credit Funds of Depository Financial Institutions (in RMB and Foreign Currency)'),
    'sources-and-uses-of-credit-funds-of-financial-institutions__sources-uses-of-credit-funds-of-depository-financial-institutions-rmb': ('Sources and Uses of Credit Funds of Financial Institutions', 'Sources & Uses of Credit Funds of Depository Financial Institutions (RMB)'),
    'sources-and-uses-of-credit-funds-of-financial-institutions__sources-uses-of-credit-funds-of-financial-institutions-in-foreign-currency': ('Sources and Uses of Credit Funds of Financial Institutions', 'Sources & Uses of Credit Funds of Financial Institutions (in Foreign Currency)'),
    'sources-and-uses-of-credit-funds-of-financial-institutions__sources-uses-of-credit-funds-of-financial-institutions-in-rmb-and-foreign-currency': ('Sources and Uses of Credit Funds of Financial Institutions', 'Sources & Uses of Credit Funds of Financial Institutions (in RMB and Foreign Currency)'),
    'sources-and-uses-of-credit-funds-of-financial-institutions__sources-uses-of-credit-funds-of-financial-institutions-rmb': ('Sources and Uses of Credit Funds of Financial Institutions', 'Sources & Uses of Credit Funds of Financial Institutions (RMB)'),
}

_DATA_TABLE = re.compile(r'<table[^>]*class="data_table"[^>]*>(.*?)</table>', re.S | re.I)
_TITLE_TD = re.compile(r'<td[^>]*align="left"[^>]*>(.*?)</td>', re.S | re.I)
_DATA_LINK = re.compile(
    r'(/[A-Za-z0-9_/]*?(?:attachDir|fileDir/resource/cms)/\d{4}/\d{2}/\d+\.(?:html?|xlsx?))', re.I)
_NAV_ANCHOR = re.compile(
    r"<a\s+href=['\"](/en/3688247/3688975/(\d+)(?:/(\d+))?/index\.html)['\"][^>]*>(.*?)</a>", re.S | re.I)
_PERIOD = re.compile(r'^(\d{4})[.\-/年]\s*(\d{1,2})\s*月?$')
_NOTE = re.compile(r'^\s*(注\s*[:：]|注\d|note|备注|资料来源|source\s*[:：])', re.I)
_UNIT = re.compile(r'unit\s*[:：]\s*(.+)', re.I)


# ---- text helpers ---------------------------------------------------------

def _clean(v) -> str:
    s = "" if v is None else str(v)
    if s == "nan":
        s = ""
    return re.sub(r"\s+", " ", s.replace("\xa0", " ").replace("　", " ")).strip()


def _strip_tags(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))


def _to_num(s: str):
    s = s.replace(",", "").replace("%", "").strip()
    if s in ("", "-", "—", "…", "..", "/", "nan", "N/A", "NA"):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def _decode(raw: bytes) -> str:
    head = raw[:1000].lower()
    if b"charset=utf-8" in head or b'encoding="utf-8"' in head:
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            pass
    for enc in ("gb18030", "utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", "replace")


# ---- grid extraction ------------------------------------------------------

def _grid_from_htm(text: str):
    import pandas as pd
    grids = [df.map(_clean).values.tolist() for df in pd.read_html(io.StringIO(text))]
    grids = [g for g in grids if g]
    return max(grids, key=lambda g: len(g) * len(g[0])) if grids else []


def _grid_from_xls(content: bytes):
    import pandas as pd
    xls = pd.ExcelFile(io.BytesIO(content))
    best = []
    for sheet in xls.sheet_names:
        g = xls.parse(sheet, header=None).map(_clean).values.tolist()
        if g and len(g) * len(g[0]) > (len(best) * len(best[0]) if best else 0):
            best = g
    return best


# ---- the generic table parser ---------------------------------------------

def _table_unit(grid, upto):
    for row in grid[:upto]:
        for cell in row:
            m = _UNIT.search(cell)
            if m:
                return m.group(1).strip() or None
    return None


def _parse_grid(grid):
    """Parse a PBOC statistical grid into long-format records:
    {item, period 'YYYY-MM', year, month, value, unit}."""
    if not grid:
        return []
    ncols = max(len(r) for r in grid)
    grid = [r + [""] * (ncols - len(r)) for r in grid]
    nrows = len(grid)

    # orientation A: a header ROW carries >=2 period labels
    for ri, row in enumerate(grid):
        pc = {ci: _PERIOD.match(c) for ci, c in enumerate(row) if _PERIOD.match(c)}
        if len(pc) >= 2:
            pcol = {ci: (int(m.group(1)), int(m.group(2))) for ci, m in pc.items()}
            return _parse_rows(grid, ri, pcol, ncols)

    # orientation B (transposed): a COLUMN carries >=2 period labels
    for ci in range(ncols):
        pr = {ri: _PERIOD.match(grid[ri][ci]) for ri in range(nrows) if _PERIOD.match(grid[ri][ci])}
        if len(pr) >= 2:
            prow = {ri: (int(m.group(1)), int(m.group(2))) for ri, m in pr.items()}
            return _parse_cols(grid, ci, prow, nrows, ncols)
    return []


def _parse_rows(grid, hdr, pcol, ncols):
    unit = _table_unit(grid, hdr)
    first_p = min(pcol)
    # measure sub-header: up to 2 rows under the period header whose period-cells
    # are non-numeric text (units / "Stock" vs "Growth Rate(%)") -> fold into item
    measure = {ci: [] for ci in pcol}
    data_start = hdr + 1
    for ri in range(hdr + 1, min(hdr + 4, len(grid))):
        row = grid[ri]
        texty = [ci for ci in pcol if row[ci] and _to_num(row[ci]) is None and not _PERIOD.match(row[ci])]
        if len(texty) >= max(2, len(pcol) // 2):
            for ci in pcol:
                if row[ci]:
                    measure[ci].append(row[ci])
            data_start = ri + 1
        else:
            break

    recs = []
    pend_lbl, pend = [], None

    def flush():
        nonlocal pend_lbl, pend
        if pend and any(v is not None for _, v in pend):
            base = " ".join(dict.fromkeys([x for x in pend_lbl if x]))
            if base:
                for ci, v in pend:
                    if v is None:
                        continue
                    y, mo = pcol[ci]
                    meas = " ".join(dict.fromkeys([m for m in measure[ci] if m]))
                    item = f"{base} | {meas}" if meas else base
                    recs.append({"item": item, "period": f"{y}-{mo:02d}",
                                 "year": y, "month": mo, "value": v, "unit": unit})
        pend_lbl, pend = [], None

    for ri in range(data_start, len(grid)):
        row = grid[ri]
        joined = " ".join(c for c in row if c)
        if not joined:
            continue
        if _NOTE.match(joined):
            break  # footnotes / growth-rate mini-tables follow
        lead = [row[ci] for ci in range(first_p) if row[ci]]
        vals = [(ci, _to_num(row[ci])) for ci in pcol]
        vt = tuple(v for _, v in vals)
        if all(v is None for v in vt):
            continue
        if pend is not None and vt == tuple(v for _, v in pend):
            pend_lbl.extend(lead)  # same data, other-language label row (rowspan artifact)
        else:
            flush()
            pend_lbl, pend = list(lead), vals
    flush()
    return recs


def _parse_cols(grid, pci, prow, nrows, ncols):
    unit = _table_unit(grid, min(prow))
    first_p = min(prow)
    item_label = {}
    for ci in range(ncols):
        if ci == pci:
            continue
        parts = [grid[ri][ci] for ri in range(first_p) if grid[ri][ci]]
        item_label[ci] = " ".join(dict.fromkeys(parts))
    recs = []
    for ri in sorted(prow):
        y, mo = prow[ri]
        for ci in range(ncols):
            if ci == pci or not item_label.get(ci):
                continue
            v = _to_num(grid[ri][ci])
            if v is None:
                continue
            recs.append({"item": item_label[ci], "period": f"{y}-{mo:02d}",
                         "year": y, "month": mo, "value": v, "unit": unit})
    return recs


# ---- portal crawling ------------------------------------------------------

def _nav():
    """Parse the Data landing nav -> {year_int: [(category_name, index_path), ...]}."""
    html = get(BASE + LANDING, timeout=60).text
    nav, cur = {}, None
    for path, _year_node, cat_node, text in _NAV_ANCHOR.findall(html):
        text = _strip_tags(text)
        if re.fullmatch(r"(19|20)\d{2}", text):
            cur = int(text)
            nav.setdefault(cur, [])
        elif cat_node and cur is not None and text:
            nav[cur].append((text, path))
    return nav


def _cat_match(a: str, b: str) -> bool:
    return a == b or a.startswith(b) or b.startswith(a)


def _table_links(page_html: str, title_norm: str):
    """Return the data-file links (htm preferred, else xls) for the data_table
    whose leading title normalizes to title_norm."""
    for tbl in _DATA_TABLE.findall(page_html):
        tm = _TITLE_TD.search(tbl)
        if not tm:
            continue
        if _norm(_strip_tags(tm.group(1))) != title_norm:
            continue
        links = list(dict.fromkeys(_DATA_LINK.findall(tbl)))
        htm = [l for l in links if l.lower().endswith(("htm", "html"))]
        return htm if htm else [l for l in links if l.lower().endswith(("xls", "xlsx"))]
    return []


# Spec id = slug + entity_id with the harness's id transform (_ -> -, lowercased).
# That collapses the "__" category/title separator to "--", so we key the lookup
# by the transformed id rather than recovering the original entity id.
_BY_SPEC = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": meta
    for eid, meta in ENTITY_META.items()
}


def fetch_one(node_id: str) -> None:
    category, title = _BY_SPEC[node_id]
    cat_norm, title_norm = _norm(category), _norm(title)

    nav = _nav()
    rows = []
    for year in sorted(nav):
        for cname, path in nav[year]:
            if not _cat_match(cat_norm, _norm(cname)):
                continue
            try:
                page = get(BASE + path, timeout=60).text
            except Exception as exc:  # one bad index page must not sink the whole table
                print(f"[{node_id}] index fetch failed {path}: {type(exc).__name__}: {exc}")
                continue
            for url in _table_links(page, title_norm):
                try:
                    raw = get(BASE + url, timeout=90).content
                    if url.lower().endswith(("htm", "html")):
                        grid = _grid_from_htm(_decode(raw))
                    else:
                        grid = _grid_from_xls(raw)
                    recs = _parse_grid(grid)
                except Exception as exc:
                    print(f"[{node_id}] parse failed {url}: {type(exc).__name__}: {exc}")
                    continue
                for r in recs:
                    r["source_year"] = year
                rows.extend(recs)
                time.sleep(0.2)  # be polite; source documents no rate limit

    if not rows:
        raise RuntimeError(f"{node_id}: no records parsed for {title!r} in category {category!r}")
    save_raw_ndjson(rows, node_id)


# ---- specs ----------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fetch_one, kind="download")
    for sid in _BY_SPEC
]


def _transform_sql(download_id: str) -> str:
    return f'''
        SELECT
            CAST(period || '-01' AS DATE) AS date,
            period,
            item,
            value,
            unit
        FROM (
            SELECT item, period, value, unit,
                   row_number() OVER (PARTITION BY item, period ORDER BY source_year DESC) AS rn
            FROM "{download_id}"
        )
        WHERE rn = 1
        ORDER BY item, date
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        fn=None,
        kind="transform",
        deps=(spec.id,),
        sql=_transform_sql(spec.id),
    )
    for spec in DOWNLOAD_SPECS
]
