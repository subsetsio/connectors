"""GACC (China Customs) — English Monthly Bulletin of customs statistics.

Mechanism (from research): `monthly_report_html` — a per-entity HTML scrape.
The entry page http://english.customs.gov.cn/statics/report/monthly.html is a
catalog whose first column names each of 19 standard statistical tables and
whose remaining columns link to one server-rendered HTML page per month under
/Statics/<guid>.html. The per-month GUIDs are opaque and are harvested from the
listing every run (they are NOT derivable).

Each entity = one standard table type. Its raw asset is the long-format MELT of
every currently-published month page for that table: one row per numeric cell,
carrying (year, month, period_label, col_header, value). This uniform shape is
robust to the wildly different per-table layouts (country / HS section / customs
regime / commodity / ...) which all share the same structure of a label column
followed by numeric value columns under 1-2 merged header rows.

Notes / constraints:
- The site is served over plain HTTP only (its HTTPS presents a self-signed /
  untrusted certificate chain). We therefore use http:// URLs directly through
  subsets_utils.get — there is no TLS to verify, so this is the rare justified
  http case, not a verify=False bypass.
- The listing exposes only the CURRENT year's published months (no incremental
  query / since filter), so we re-pull the available month pages in full each
  run (stateless full re-pull — the simplest correct shape here). Cheap: ~19
  tables x a handful of months.
- The summary annual/monthly tables (table 1A/1B) are full time series whose
  own date lives in `period_label`; their per-page `month` is just the
  publication month. The per-breakdown tables (country, HS, commodity, ...) are
  per-month snapshots where `month` IS the data month. The transform keeps both
  honest with a long-format projection and a DISTINCT collapse of exact repeats.
"""

import html
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

SLUG = "china-customs-gacc"
LISTING_URL = "http://english.customs.gov.cn/statics/report/monthly.html"

# The 19 standard bulletin tables (the entity union). Ids are re-derived from
# the listing each run and matched against this set, so a layout change that
# drops/renames a table surfaces as a clear failure rather than silent drift.
ENTITY_IDS = [
    "table-01-summary-of-imports-and-exports-in-usd-a-annually",
    "table-01-summary-of-imports-and-exports-in-usd-b-monthly",
    "table-02-imports-and-exports-by-country-region-of-origin-destination",
    "table-03-composition-of-imports-and-exports-by-section-and-division",
    "table-04-imports-and-exports-by-hs-section-and-division",
    "table-05-imports-and-exports-by-customs-regime",
    "table-06-exports-by-type-enterprise-and-by-customs-regime",
    "table-07-imports-by-type-enterprise-and-by-customs-regime",
    "table-08-imports-and-exports-by-location-of-importers-exporters",
    "table-09-imports-and-exports-by-location-of-domestic-consumers-producers",
    "table-10-imports-and-exports-by-customs-districts",
    "table-11-imports-and-exports-by-specific-areas",
    "table-12-imports-and-exports-by-foreign-invested-enterprises",
    "table-13-major-export-commodities-in-quantity-and-value",
    "table-14-major-import-commodities-in-quantity-and-value",
    "table-15-exports-by-selected-countries-regions-and-by-hs-divisions",
    "table-16-imports-by-selected-countries-regions-and-by-hs-divisions",
    "table-17-exports-of-selected-commodities-by-major-customs-regimes",
    "table-18-imports-of-selected-commodities-by-major-customs-regimes",
]

_MONTHS = {
    m: i
    for i, m in enumerate(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1
    )
}

SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("period_label", pa.string()),
    ("col_header", pa.string()),
    ("value", pa.float64()),
    ("source_url", pa.string()),
])


# ---------------------------------------------------------------------------
# HTTP with the canonical retry shape
# ---------------------------------------------------------------------------


@transient_retry()
def _fetch_html(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    # The pages are GB/UTF-8 mixed; httpx usually decodes fine, but force a
    # tolerant decode so a stray byte never aborts a whole table.
    resp.encoding = resp.encoding or "utf-8"
    return resp.text


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def _parse_listing(listing_html: str) -> dict:
    """Map each table-type entity id -> list of (month_int, page_url)."""
    out = {}
    for tr in re.findall(r"<tr.*?</tr>", listing_html, re.S):
        tds = re.findall(r"<td.*?</td>", tr, re.S)
        if not tds:
            continue
        first = _clean(tds[0])
        m = re.match(r"（\s*(\d+)\s*）\s*(.*)", first)
        if not m:
            continue
        num, rest = m.group(1), m.group(2).strip()
        eid = f"table-{int(num):02d}-{_slug(rest)}"
        links = []
        for url, mon in re.findall(
            r'href=["\']?([^"\'> ]+\.html)["\']?[^>]*>\s*([A-Za-z]{3})', tr
        ):
            mi = _MONTHS.get(mon.title())
            if mi:
                links.append((mi, html.unescape(url)))
        # disambiguate when the same num/rest appears twice (table 1 A & B)
        key = eid
        suffix = 2
        while key in out:
            key = f"{eid}-{suffix}"
            suffix += 1
        out[key] = links
    return out


def _expand_grid(table_html: str) -> list:
    """Expand a single <table> into a dense matrix, honouring col/rowspan."""
    grid, pending = [], {}
    for tr in re.findall(r"<tr.*?</tr>", table_html, re.S):
        cells = re.findall(r"<t[dh]\b([^>]*)>(.*?)</t[dh]>", tr, re.S)
        row, col = [], 0
        for attrs, inner in cells:
            while col in pending:
                txt, rem = pending[col]
                row.append(txt)
                pending[col] = (txt, rem - 1)
                if rem - 1 <= 0:
                    del pending[col]
                col += 1
            mcs = re.search(r'colspan="?(\d+)', attrs)
            mrs = re.search(r'rowspan="?(\d+)', attrs)
            cs = int(mcs.group(1)) if mcs else 1
            rs = int(mrs.group(1)) if mrs else 1
            txt = _clean(inner)
            for _ in range(cs):
                row.append(txt)
                if rs > 1:
                    pending[col] = (txt, rs - 1)
                col += 1
        while col in pending:
            txt, rem = pending[col]
            row.append(txt)
            pending[col] = (txt, rem - 1)
            if rem - 1 <= 0:
                del pending[col]
            col += 1
        grid.append(row)
    return grid


def _to_num(s: str):
    s = s.replace(",", "").replace("\xa0", "").strip()
    if s in ("", "-", "—", "…", "±", "/"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _is_strong(cell: str) -> bool:
    """A real datum (has a thousands/decimal separator or magnitude >= 10),
    as opposed to a footnote marker or column number in a header row."""
    v = _to_num(cell)
    if v is None:
        return False
    return ("," in cell) or ("." in cell) or abs(v) >= 10


def _parse_page(page_html: str, month_hint: int) -> list:
    mt = re.search(r"<table.*?</table>", page_html, re.S)
    if not mt:
        return []
    grid = _expand_grid(mt.group(0))

    title_m = re.search(r"<title>(.*?)</title>", page_html, re.S)
    title = _clean(title_m.group(1)) if title_m else ""
    ym = re.search(r"(19|20)\d{2}", title)
    year = int(ym.group(0)) if ym else None

    def is_title_row(r):
        ne = [c for c in r if c.strip()]
        return len(ne) > 1 and len(set(ne)) == 1

    def is_unit_row(r):
        ne = [c for c in r if c.strip()]
        return bool(ne) and all("unit" in c.lower() for c in ne)

    def is_data_row(r):
        return bool(r) and r[0].strip() != "" and any(_is_strong(c) for c in r[1:])

    data_idx = [i for i, r in enumerate(grid) if is_data_row(r)]
    if not data_idx:
        return []
    first = min(data_idx)
    headers = [
        r for i, r in enumerate(grid)
        if i < first and len(r) > 1 and not is_title_row(r) and not is_unit_row(r)
    ]

    def col_header(c):
        parts = []
        for hr in headers:
            if c < len(hr):
                p = hr[c].strip()
                # drop pure-digit header tokens (footnote markers / col numbers)
                if p and not re.fullmatch(r"\d+", p) and (not parts or parts[-1] != p):
                    parts.append(p)
        return " | ".join(parts)

    rows = []
    for i in data_idx:
        r = grid[i]
        label = r[0].strip()
        if not label:
            continue
        for c in range(1, len(r)):
            v = _to_num(r[c])
            if v is None:
                continue
            rows.append({
                "year": year,
                "month": month_hint,
                "period_label": label,
                "col_header": col_header(c),
                "value": v,
            })
    return rows


# ---------------------------------------------------------------------------
# Download — one shared fetch per entity
# ---------------------------------------------------------------------------
def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity_id = node_id[len(SLUG) + 1:]  # strip "china-customs-gacc-"

    listing = _fetch_html(LISTING_URL)
    table_map = _parse_listing(listing)
    months = table_map.get(entity_id)
    if not months:
        raise RuntimeError(
            f"{asset}: no month pages found for entity '{entity_id}' in the "
            f"listing (known: {sorted(table_map)[:3]}...). Listing layout may "
            f"have changed."
        )

    rows = []
    for month_int, url in months:
        page = _fetch_html(url)
        page_rows = _parse_page(page, month_int)
        for pr in page_rows:
            pr["source_url"] = url
        rows.extend(page_rows)

    if not rows:
        raise RuntimeError(
            f"{asset}: parsed 0 data rows across {len(months)} month page(s); "
            f"page layout may have changed."
        )

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


# ---------------------------------------------------------------------------
# Transform — one published long-format table per entity
# ---------------------------------------------------------------------------
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT DISTINCT
                year,
                month,
                period_label,
                col_header AS indicator,
                value
            FROM "{s.id}"
            WHERE value IS NOT NULL
              AND period_label IS NOT NULL
              AND period_label <> ''
        ''',
    )
    for s in DOWNLOAD_SPECS
]
