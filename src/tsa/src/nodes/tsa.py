"""TSA connector — Checkpoint Travel Numbers (daily national passenger throughput).

Single subset: the daily count of passengers screened at all U.S. TSA airport
security checkpoints (national total), 2019-01-01 to present.

Mechanism (from research): static-HTML scrape of
https://www.tsa.gov/travel/passenger-volumes . The base page carries the
*current* year's daily rows in one two-column HTML table ('Date', 'Numbers')
AND links to one persistent per-year page per prior year
(/travel/passenger-volumes/<year>, 2019..last-year). We discover the year set
from those links rather than hardcoding a range, then union the base-page
(current year) table with every discovered year page. There is no bulk export,
no incremental query filter, and the whole corpus is tiny (~2700 daily rows),
so this is a stateless full re-pull every run (shape 1) — no state, no cursor.

The richer hourly-by-airport throughput product is published only as weekly
PDFs (TSA FOIA Reading Room) and is intentionally not covered here.

EGRESS NOTE: tsa.gov's Akamai edge serves the pages fine to ordinary IPs
(verified locally, even with a bot User-Agent) but returns 403 Forbidden to
the cloud CI runner's datacenter IP — regardless of User-Agent. There is no
official API and no maintained cloud-reachable mirror for the daily series, so
a production run must egress through a non-datacenter proxy. Setting the
standard ``HTTPS_PROXY`` env var to such a proxy is sufficient: the
``subsets_utils`` httpx client runs with ``trust_env=True`` (default), so it
routes through ``HTTPS_PROXY`` automatically with no code change. The connector
is harness-blocked on that env var until it is provisioned.
"""
from __future__ import annotations

import datetime as _dt
import re

import lxml.html as LH
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE_URL = "https://www.tsa.gov/travel/passenger-volumes"
_YEAR_LINK_RE = re.compile(r"/travel/passenger-volumes/(\d{4})\b")

# TSA returns 403 to the library's default bot User-Agent (observed from the
# cloud runner). Present as a real browser. ASCII-only header values.
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

SCHEMA = pa.schema(
    [
        ("date", pa.date32()),
        ("passengers", pa.int64()),
        ("source_year", pa.int32()),  # the page the row was scraped from
    ]
)


@transient_retry()
def _fetch_html(url: str) -> str:
    resp = get(url, headers=_BROWSER_HEADERS, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _parse_table(html: str, url: str) -> list[tuple[_dt.date, int]]:
    """Parse the single two-column ('Date', 'Numbers') table on a TSA
    passenger-volumes page into (date, passengers) tuples."""
    doc = LH.fromstring(html)
    tables = doc.xpath("//table")
    if not tables:
        raise AssertionError(f"no <table> found on {url} (page format changed?)")
    rows: list[tuple[_dt.date, int]] = []
    for tr in tables[0].xpath(".//tr"):
        cells = [td.text_content().strip() for td in tr.xpath("./td")]
        if len(cells) != 2:
            continue  # header row (<th>) or layout row
        date_txt, num_txt = cells
        if not date_txt or not num_txt:
            continue
        d = _dt.datetime.strptime(date_txt, "%m/%d/%Y").date()
        passengers = int(num_txt.replace(",", "").strip())
        rows.append((d, passengers))
    return rows


def fetch_passenger_volumes(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    base_html = _fetch_html(BASE_URL)

    # The base page holds the current year's rolling table.
    seen: dict[_dt.date, tuple[_dt.date, int, int]] = {}
    for d, p in _parse_table(base_html, BASE_URL):
        seen[d] = (d, p, d.year)

    # Discover the per-year pages linked from the base page (2019..last-year).
    years = sorted({int(y) for y in _YEAR_LINK_RE.findall(base_html)})
    if not years:
        raise AssertionError(
            f"no per-year links discovered on {BASE_URL} (page format changed?)"
        )

    for year in years:
        url = f"{BASE_URL}/{year}"
        rows = _parse_table(_fetch_html(url), url)
        if not rows:
            raise AssertionError(f"{url}: table parsed to 0 rows")
        for d, p in rows:
            # Year pages and the base page do not overlap in practice (base =
            # current year, year pages = prior years), but key on date so any
            # accidental overlap collapses to one row.
            seen.setdefault(d, (d, p, year))

    if not seen:
        raise AssertionError("parsed 0 total rows across all pages")

    ordered = sorted(seen.values(), key=lambda r: r[0])
    table = pa.table(
        {
            "date": pa.array([r[0] for r in ordered], type=pa.date32()),
            "passengers": pa.array([r[1] for r in ordered], type=pa.int64()),
            "source_year": pa.array([r[2] for r in ordered], type=pa.int32()),
        },
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="tsa-passenger-volumes",
        fn=fetch_passenger_volumes,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="tsa-passenger-volumes-transform",
        deps=["tsa-passenger-volumes"],
        key=("date",),
        temporal="date",
        sql='''
            SELECT
                CAST(date AS DATE)        AS date,
                CAST(passengers AS BIGINT) AS passengers
            FROM "tsa-passenger-volumes"
            WHERE date IS NOT NULL
              AND passengers IS NOT NULL
              AND passengers > 0
            QUALIFY row_number() OVER (PARTITION BY date ORDER BY passengers DESC) = 1
            ORDER BY date
        ''',
    ),
]
