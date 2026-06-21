"""Adobe connector — Digital Economy Index (DEI) and Digital Price Index (DPI).

Adobe publishes two public statistical data products as per-chart JSON 'sheet'
files on its Edge Delivery origin (the canonical business.adobe.com portal is
Akamai bot-blocked). There is no API, no bulk export, and no index/manifest.

Path scheme:
    {ORIGIN}/assets/charts/resources/{product}/{YYYY}/{mon}/{chart-slug}.json

Each chart file is a rolling window:
  - DEI charts return ~10-13 trailing months of (date, value) rows. Successive
    monthly files overlap heavily, so we crawl month directories backward and
    concatenate, deduping by the parsed date (keeping the most recent file's
    value, which absorbs revisions).
  - DPI's category chart is a single-month wide snapshot (one row, columns =
    product categories). Each month is its own file with no overlap, so crawling
    months back reconstructs the time series; the reference date comes from the
    file path (the row's 'month' field carries only a month name, no year).

Fetch shape: stateless full re-pull. The corpus is tiny (5 charts, a few dozen
GETs each) so we re-fetch the entire history every run and overwrite — revisions
are picked up for free. No incremental query is supported by the source.

Discovery: the chart slug carries a drifting numeric prefix and is not indexed,
so for each entity we read the product's canonical `.plain.html` (which always
references the latest published month's charts) to recover the current slug +
latest month, then walk months backward trying that slug. The numeric prefix is
stable per chart across the months that exist; months that 404 are skipped.

Fragility caveat: the aem.live origin host is undocumented and internal; if Adobe
moves it the fetch fails loudly (no silent fallback).
"""

import re

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

ORIGIN = "https://main--da-bacom--adobecom.aem.live"
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]
MONTH_NUM = {m: i + 1 for i, m in enumerate(MONTHS)}

PRODUCTS = {"dei": "digital-economy-index", "dpi": "digital-price-index"}

# Stop crawling backward after this many consecutive missing months (one full
# rolling window's worth + margin) — that means we are past the series start.
MAX_CONSECUTIVE_MISSES = 15
# Absolute safety ceiling on how far back we walk; firing means the source grew
# unexpectedly (or the miss-detection broke) — raise rather than loop forever.
MAX_MONTHS_LOOKBACK = 180


def _spec_to_target(node_id: str) -> tuple:
    """adobe-dei-monthly-online-spending -> ('digital-economy-index', 'monthly-online-spending')."""
    rest = node_id[len("adobe-"):]
    prefix, base = rest.split("-", 1)
    return PRODUCTS[prefix], base


@transient_retry()
def _get_json_or_none(url: str):
    """GET a chart file. 404 (month/slug absent) is an expected, non-error
    outcome → return None; transient/5xx are retried; other 4xx raise."""
    resp = get(url, timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _discover_latest(product: str, base: str):
    """Read the product's canonical page and return (year, mon, slug) for the
    chart whose numeric-prefix-stripped slug matches `base`, picking the most
    recent month referenced."""
    html = _get_text(f"{ORIGIN}/resources/{product}.plain.html")
    pat = re.escape(product) + r"/(\d{4})/([a-z]{3})/([A-Za-z0-9\-]+)\.json"
    best = None
    for year, mon, slug in re.findall(pat, html):
        if mon not in MONTH_NUM:
            continue
        if re.sub(r"^\d+-", "", slug) != base:
            continue
        key = (int(year), MONTH_NUM[mon])
        if best is None or key > best[0]:
            best = (key, year, mon, slug)
    return None if best is None else (best[1], best[2], best[3])


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    product, base = _spec_to_target(node_id)

    latest = _discover_latest(product, base)
    if latest is None:
        raise RuntimeError(
            f"{node_id}: chart '{base}' not found on {product} page — "
            f"slug naming or origin likely changed"
        )
    ly, lm, slug = latest

    rows = []
    year, mi = int(ly), MONTH_NUM[lm] - 1
    misses = 0
    stepped = 0
    while misses < MAX_CONSECUTIVE_MISSES:
        if stepped > MAX_MONTHS_LOOKBACK:
            raise RuntimeError(
                f"{node_id}: exceeded {MAX_MONTHS_LOOKBACK}-month lookback "
                f"safety cap — source may have changed"
            )
        mon = MONTHS[mi]
        url = f"{ORIGIN}/assets/charts/resources/{product}/{year}/{mon}/{slug}.json"
        doc = _get_json_or_none(url)
        if doc is not None:
            misses = 0
            file_ym = f"{year}-{mon}"
            file_date = f"{year}-{MONTH_NUM[mon]:02d}-01"
            for row in doc.get("data", []):
                if not isinstance(row, dict):
                    continue
                enriched = dict(row)
                enriched["_file_ym"] = file_ym
                enriched["_file_date"] = file_date
                rows.append(enriched)
        else:
            misses += 1
        mi -= 1
        if mi < 0:
            mi = 11
            year -= 1
        stepped += 1

    if not rows:
        raise RuntimeError(
            f"{node_id}: crawl found slug '{slug}' on the page but no month "
            f"file returned data rows"
        )
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="adobe-dei-monthly-online-spending", fn=fetch_one, kind="download"),
    NodeSpec(id="adobe-dei-year-over-year-growth-in-online-spend", fn=fetch_one, kind="download"),
    NodeSpec(id="adobe-dei-buy-now-pay-later-monthly-spend", fn=fetch_one, kind="download"),
    NodeSpec(id="adobe-dei-total-dollars-spent-through-bnpl", fn=fetch_one, kind="download"),
    NodeSpec(id="adobe-dpi-columnchart-dpi-percent-change", fn=fetch_one, kind="download"),
]


# Date in DEI rows is either an "M/D/YY" string or an Excel serial integer
# (the chart data mixes both). Parse both; Excel epoch is 1899-12-30.
def _date_expr(col: str) -> str:
    return (
        f"COALESCE("
        f"try_strptime({col}, '%-m/%-d/%y')::DATE, "
        f"CASE WHEN try_cast({col} AS INTEGER) IS NOT NULL "
        f"THEN DATE '1899-12-30' + try_cast({col} AS INTEGER) END)"
    )


def _dei_series_sql(asset: str, date_col: str, value_col: str) -> str:
    d = _date_expr(date_col)
    return f'''
        SELECT date, value
        FROM (
            SELECT
                {d} AS date,
                TRY_CAST({value_col} AS DOUBLE) AS value,
                row_number() OVER (PARTITION BY {d} ORDER BY _file_date DESC) AS rn
            FROM "{asset}"
            WHERE {date_col} IS NOT NULL
        )
        WHERE rn = 1 AND date IS NOT NULL AND value IS NOT NULL
        ORDER BY date
    '''


_DPI_ASSET = "adobe-dpi-columnchart-dpi-percent-change"
_DPI_SQL = f'''
    SELECT
        CAST(_file_date AS DATE) AS date,
        category,
        TRY_CAST(val AS DOUBLE) AS percent_change
    FROM (
        UNPIVOT "{_DPI_ASSET}"
        ON COLUMNS(* EXCLUDE ("month", "_file_ym", "_file_date"))
        INTO NAME category VALUE val
    )
    WHERE TRY_CAST(val AS DOUBLE) IS NOT NULL
    ORDER BY date, category
'''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="adobe-dei-monthly-online-spending-transform",
        deps=["adobe-dei-monthly-online-spending"],
        sql=_dei_series_sql("adobe-dei-monthly-online-spending", '"Date"', '"Spend in billions"'),
    ),
    SqlNodeSpec(
        id="adobe-dei-year-over-year-growth-in-online-spend-transform",
        deps=["adobe-dei-year-over-year-growth-in-online-spend"],
        sql=_dei_series_sql("adobe-dei-year-over-year-growth-in-online-spend", '"Date"', '"Growth"'),
    ),
    SqlNodeSpec(
        id="adobe-dei-buy-now-pay-later-monthly-spend-transform",
        deps=["adobe-dei-buy-now-pay-later-monthly-spend"],
        sql=_dei_series_sql("adobe-dei-buy-now-pay-later-monthly-spend", '"Date"', '"Spend in billions"'),
    ),
    SqlNodeSpec(
        id="adobe-dei-total-dollars-spent-through-bnpl-transform",
        deps=["adobe-dei-total-dollars-spent-through-bnpl"],
        sql=_dei_series_sql("adobe-dei-total-dollars-spent-through-bnpl", '"date"', '"Growth"'),
    ),
    SqlNodeSpec(
        id="adobe-dpi-columnchart-dpi-percent-change-transform",
        deps=[_DPI_ASSET],
        sql=_DPI_SQL,
    ),
]
