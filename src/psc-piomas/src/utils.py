"""Shared HTTP + parsing helpers for the PIOMAS connector.

The monthly product fetches a stable CSV URL; the two daily products discover
their year-stamped .dat.gz URL from the project data page, gunzip it, and parse
the whitespace-separated 'Year #day Value' format.
"""

import datetime as dt
import gzip
import re

import httpx

from subsets_utils import get, transient_retry

DATA_PAGE = (
    "https://psc.apl.uw.edu/research/projects/"
    "arctic-sea-ice-volume-anomaly/data/"
)


@transient_retry()
def fetch(url: str) -> httpx.Response:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def discover_daily_url(product: str) -> str:
    """Find the current daily .dat.gz URL for 'vol' or 'thick' on the data
    page. The filenames embed the end year, which rolls forward annually."""
    html = fetch(DATA_PAGE).text
    pat = re.compile(
        r'href="([^"]+PIOMAS\.' + re.escape(product) + r'\.daily\.[^"]+\.dat\.gz)"'
    )
    m = pat.search(html)
    if not m:
        raise RuntimeError(
            f"could not locate the daily {product} .dat.gz link on {DATA_PAGE}"
        )
    return m.group(1)


def gunzip(raw: bytes) -> str:
    try:
        return gzip.decompress(raw).decode("utf-8", errors="replace")
    except gzip.BadGzipFile:
        # Server may have already content-decoded the stream.
        return raw.decode("utf-8", errors="replace")


def parse_daily(text: str, value_key: str) -> list[dict]:
    """Whitespace-separated 'Year #day Value'. #day is day-of-year (1..366)."""
    rows: list[dict] = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 3 or not parts[0].isdigit():
            continue  # skips the 'Year #day Vol' header and blanks
        year, doy = int(parts[0]), int(parts[1])
        try:
            value = float(parts[2])
        except ValueError:
            continue
        if value < 0:
            continue  # missing-value sentinel
        date = dt.date(year, 1, 1) + dt.timedelta(days=doy - 1)
        rows.append({"date": date, value_key: value})
    return rows
