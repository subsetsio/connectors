"""Shared helpers for the Robert Shiller (Yale) connector.

Source: shillerdata.com -- Robert J. Shiller's long-run datasets, formerly hosted
at the Yale econ faculty page (www.econ.yale.edu/~shiller/data.htm, now defunct).

Fetch strategy (per research 'shiller_xls'): the wsimg.com CDN download UUIDs
rotate on re-upload, so we GET the shillerdata.com landing page and scrape the
.xls hrefs each run rather than hardcoding URLs. Legacy BIFF .xls is parsed with
pandas+xlrd in the download fn (DuckDB/openpyxl cannot read it); each fetch writes
a tidy typed parquet that the SQL transform thinly casts/projects.

Stateless full re-pull every run: the corpus is ~2 MB and Shiller restates each
workbook in full on every (roughly monthly) update, so there is no incremental
filter to use and revisions are picked up for free.
"""

import math
import re

import httpx

from subsets_utils import get, transient_retry

LANDING = "https://shillerdata.com/"


@transient_retry()
def _http_get(url: str) -> httpx.Response:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def _resolve_xls(name_substr: str) -> str:
    """Scrape the shillerdata.com landing page for the .xls download whose
    filename contains `name_substr` (case-insensitive). The wsimg CDN UUIDs
    rotate on re-upload, so the URL must be discovered, not hardcoded."""
    html = _http_get(LANDING).text
    urls = sorted({
        "https:" + m
        for m in re.findall(r'(//img1\.wsimg\.com/blobby/go/[^"\']+?\.xls)', html)
    })
    for u in urls:
        if name_substr.lower() in u.lower():
            return u
    raise RuntimeError(
        f"could not find an .xls link matching '{name_substr}' on {LANDING} "
        f"(found: {urls})"
    )


def _isnum(v) -> bool:
    return isinstance(v, (int, float)) and not (isinstance(v, float) and math.isnan(v))


def _num(v):
    """Cell -> float or None (treats blanks / 'NA' / text as missing)."""
    if _isnum(v):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v.strip())
        except ValueError:
            return None
    return None


def _decode_date(v):
    """Shiller decimal-year cell -> 'YYYY-MM-01'.

    The workbooks mix three encodings, sometimes within one file:
      - integer year (annual obs)               -> Jan 1 of that year
      - year.month, fraction*100 in 1..12       -> that month (ie_data.xls)
      - decimal year-fraction, (month-0.5)/12   -> that month (home-price file)
    Returns None for non-date cells (header/footnote rows)."""
    if not _isnum(v) or not (1700 < v < 2200):
        return None
    yr = int(round(v)) if abs(v - round(v)) < 1e-9 else int(math.floor(v))
    frac = v - yr
    if frac < 1e-6:
        return f"{yr:04d}-01-01"
    h = frac * 100
    if abs(h - round(h)) < 1e-3 and 1 <= round(h) <= 12:
        mo = round(h)
    else:
        mo = max(1, min(12, round(frac * 12 + 0.5)))
    return f"{yr:04d}-{mo:02d}-01"
