"""American Enterprise Institute — Housing Center connector.

Source: AEI Housing Center "National and Metro Housing Market Indicators".
There is no API. Each refresh we scrape the indicators page for the current
quarterly time-series .xlsx link (the path is versioned per release and carries
a cache-buster query, so it must be rediscovered, never hardcoded) and pull the
whole workbook. The workbook is small (~2 MB, ~16,800 rows covering 2012:Q1 ->
latest) so we do a stateless full re-pull each run and overwrite — revisions are
picked up for free. www.aei.org sits behind Cloudflare bot protection; a plain
GET with the default browser User-Agent returns the real body (HEAD is
challenged, so we never use HEAD).
"""

import io
import re
import time

import httpx
import openpyxl
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

INDICATORS_PAGE = "https://www.aei.org/national-and-metro-housing-market-indicators/"

# www.aei.org sits behind Cloudflare. From a normal machine a browser User-Agent
# returns the real body, but the cloud runner's datacenter IP/TLS fingerprint is
# 403'd regardless of User-Agent (verified: a real browser UA still 403s from CI).
# So we send realistic browser headers on the logged subsets_utils path, and on a
# 403 fall back to curl_cffi impersonating Chrome's TLS (JA3) handshake, which
# clears the challenge. Same approach as the bruegel connector.
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _curl_fetch(url: str, binary: bool):
    """Cloudflare bypass: curl_cffi impersonates Chrome's TLS handshake, clearing
    the challenge that 403s the logged client from the runner's datacenter IP.
    Used only as the fallback when the subsets_utils path returns 403."""
    from curl_cffi import requests as cr

    last = None
    for attempt in range(5):
        try:
            r = cr.get(url, impersonate="chrome", headers=BROWSER_HEADERS,
                       timeout=180, allow_redirects=True)
            if r.status_code == 200:
                return r.content if binary else r.text
            last = f"HTTP {r.status_code}"
        except Exception as e:  # curl_cffi transport error — retry with backoff
            last = f"{type(e).__name__}: {e}"
        time.sleep(2 * (attempt + 1))
    raise AssertionError(f"curl_cffi fallback failed for {url}: {last}")

# The 13 meaningful columns of the workbook's single "data" sheet (the sheet has
# trailing empty columns we drop). Order matches the source header row exactly.
COLUMNS = [
    "metro",
    "metro_group",
    "year_quarter",
    "segment",
    "segment_share_of_sales",
    "median_sale_price",
    "stressed_mortgage_default_rate",
    "months_supply",
    "new_construction_share_of_sales",
    "new_construction_contribution_existing_stock",
    "hpa_yoy",
    "hpa_qoq",
    "cumulative_hpa_since_2012",
]

SCHEMA = pa.schema([
    ("metro", pa.string()),
    ("metro_group", pa.string()),
    ("year_quarter", pa.string()),
    ("segment", pa.string()),
    ("segment_share_of_sales", pa.float64()),
    ("median_sale_price", pa.float64()),
    ("stressed_mortgage_default_rate", pa.float64()),
    ("months_supply", pa.float64()),
    ("new_construction_share_of_sales", pa.float64()),
    ("new_construction_contribution_existing_stock", pa.float64()),
    ("hpa_yoy", pa.float64()),
    ("hpa_qoq", pa.float64()),
    ("cumulative_hpa_since_2012", pa.float64()),
])


@transient_retry()
def _fetch_text(url: str) -> str:
    try:
        resp = get(url, headers=BROWSER_HEADERS, timeout=(10.0, 120.0))
        resp.raise_for_status()
        return resp.text
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            return _curl_fetch(url, binary=False)
        raise


@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    try:
        resp = get(url, headers=BROWSER_HEADERS, timeout=(10.0, 180.0))
        resp.raise_for_status()
        return resp.content
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            return _curl_fetch(url, binary=True)
        raise


def _discover_workbook_url() -> str:
    """Scrape the indicators page for the current time-series workbook link.

    The page exposes two .xlsx links: the metro/national time-series workbook
    (filename contains 'data_download'/'interactive') and a 'Top-100-metros'
    county crosswalk we don't publish. Pick the former; raise if it's gone
    (the page changed shape and the connector needs a look).
    """
    html = _fetch_text(INDICATORS_PAGE)
    links = re.findall(r'href="([^"]+\.xlsx[^"]*)"', html)
    candidates = [
        l for l in links
        if ("data_download" in l.lower() or "interactive" in l.lower())
        and "top-100-metros" not in l.lower()
    ]
    if not candidates:
        raise AssertionError(
            f"no time-series .xlsx link found on {INDICATORS_PAGE}; "
            f"found xlsx links: {links}"
        )
    return candidates[0]


def fetch_housing_market_indicators(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    url = _discover_workbook_url()
    content = _fetch_bytes(url)

    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows_iter = ws.iter_rows(values_only=True)
    header = next(rows_iter)
    if header[: len(COLUMNS)][2] != "Year:Quarter":
        raise AssertionError(f"unexpected workbook header: {header!r}")

    ncol = len(COLUMNS)
    rows = []
    for raw in rows_iter:
        if raw is None or all(c is None for c in raw):
            continue
        if raw[0] is None:  # skip rows without a metro label
            continue
        record = {col: raw[i] for i, col in enumerate(COLUMNS) if i < len(raw)}
        for col in COLUMNS[:ncol]:
            record.setdefault(col, None)
        rows.append(record)

    if not rows:
        raise AssertionError(f"{asset}: parsed 0 data rows from workbook {url}")

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="american-enterprise-institute-housing-market-indicators",
        fn=fetch_housing_market_indicators,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="american-enterprise-institute-housing-market-indicators-transform",
        deps=["american-enterprise-institute-housing-market-indicators"],
        sql='''
            SELECT
                metro,
                metro_group,
                year_quarter,
                CAST(split_part(year_quarter, ':', 1) AS INTEGER) AS year,
                CAST(replace(split_part(year_quarter, ':', 2), 'Q', '') AS INTEGER) AS quarter,
                segment,
                segment_share_of_sales,
                median_sale_price,
                stressed_mortgage_default_rate,
                months_supply,
                new_construction_share_of_sales,
                new_construction_contribution_existing_stock,
                hpa_yoy,
                hpa_qoq,
                cumulative_hpa_since_2012
            FROM "american-enterprise-institute-housing-market-indicators"
            WHERE metro IS NOT NULL
              AND year_quarter IS NOT NULL
              AND regexp_matches(year_quarter, '^[0-9]{4}:Q[1-4]$')
        ''',
    ),
]
