"""Ivey Purchasing Managers Index connector.

Source: https://iveypmi.uwo.ca/historic-data/ (Ivey Business School, Western
University). Mechanism: scrape (static HTML) — chosen by research; the only
verifiable machine-readable surface. The page server-renders two HTML tables —
"Seasonally Adjusted" and "Not Seasonally Adjusted" — each with the same five
monthly index columns (the headline Ivey PMI plus Employment, Inventories,
Deliveries and Prices sub-indices), keyed by month (M/YYYY).

Fetch shape: stateless full re-pull. A single GET returns every value the page
exposes (a rolling ~24-month window per the source; full 2001-present history is
described but not downloadable). No incremental filter exists and the payload is
tiny (<100 KB), so we re-fetch and overwrite every run — revisions are picked up
for free. One download node for the single catalog entity; one transform that
publishes the wide monthly table (date + seasonal_adjustment + 5 index columns).
"""

import datetime as dt

import pyarrow as pa
from lxml import html

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

HISTORIC_URL = "https://iveypmi.uwo.ca/historic-data/"

# Source column label (in table order) -> our snake_case raw column.
INDEX_LABELS = [
    "Ivey PMI",
    "Employment Index",
    "Inventories Index",
    "Deliveries Index",
    "Prices Index",
]
INDEX_COLS = [
    "ivey_pmi",
    "employment_index",
    "inventories_index",
    "deliveries_index",
    "prices_index",
]

SCHEMA = pa.schema(
    [
        ("date", pa.date32()),
        ("seasonal_adjustment", pa.string()),
        ("ivey_pmi", pa.float64()),
        ("employment_index", pa.float64()),
        ("inventories_index", pa.float64()),
        ("deliveries_index", pa.float64()),
        ("prices_index", pa.float64()),
    ]
)


@transient_retry()  # 6 attempts, exponential backoff, reraise
def _get_html(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _parse_float(text: str):
    text = (text or "").strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _parse_month(text: str):
    """'5/2026' -> date(2026, 5, 1). Returns None for a non-date cell."""
    text = (text or "").strip()
    parts = text.split("/")
    if len(parts) != 2:
        return None
    month, year = parts
    if not (month.isdigit() and year.isdigit()):
        return None
    return dt.date(int(year), int(month), 1)


def _adjustment_for_table(table) -> str:
    """Associate a table with its nearest preceding section heading.

    The `preceding::` axis excludes ancestors, and matching on a *direct* text
    node (text()) excludes container <div>s whose text_content merely contains
    the label — so this reliably picks the section label that introduces this
    table rather than guessing from table order.
    """
    labels = table.xpath(
        "preceding::*[text()[normalize-space()='Seasonally Adjusted' "
        "or normalize-space()='Not Seasonally Adjusted']]"
    )
    if not labels:
        raise AssertionError("no seasonal-adjustment heading found for a table")
    nearest = labels[-1].text_content().strip()
    return (
        "not_seasonally_adjusted"
        if nearest == "Not Seasonally Adjusted"
        else "seasonally_adjusted"
    )


def fetch_ivey_pmi(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    doc = html.fromstring(_get_html(HISTORIC_URL))

    tables = doc.xpath("//table")
    assert len(tables) == 2, f"expected 2 data tables, found {len(tables)}"

    rows = []
    for table in tables:
        adjustment = _adjustment_for_table(table)
        for tr in table.xpath(".//tr"):
            cells = [c.text_content().strip() for c in tr.xpath("./th|./td")]
            if len(cells) < 1 + len(INDEX_COLS):
                continue  # spacer / malformed row
            date = _parse_month(cells[0])
            if date is None:
                continue  # header row or non-data row
            row = {"date": date, "seasonal_adjustment": adjustment}
            for col, raw in zip(INDEX_COLS, cells[1 : 1 + len(INDEX_COLS)]):
                row[col] = _parse_float(raw)
            rows.append(row)

    assert rows, "parsed zero data rows from historic-data page"
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="ivey-purchasing-managers-index-ivey-pmi",
        fn=fetch_ivey_pmi,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ivey-purchasing-managers-index-ivey-pmi-transform",
        deps=["ivey-purchasing-managers-index-ivey-pmi"],
        sql='''
            SELECT
                CAST(date AS DATE)                  AS date,
                seasonal_adjustment,
                CAST(ivey_pmi AS DOUBLE)            AS ivey_pmi,
                CAST(employment_index AS DOUBLE)    AS employment_index,
                CAST(inventories_index AS DOUBLE)   AS inventories_index,
                CAST(deliveries_index AS DOUBLE)    AS deliveries_index,
                CAST(prices_index AS DOUBLE)        AS prices_index
            FROM "ivey-purchasing-managers-index-ivey-pmi"
            WHERE date IS NOT NULL
              AND ivey_pmi IS NOT NULL
        ''',
    ),
]
