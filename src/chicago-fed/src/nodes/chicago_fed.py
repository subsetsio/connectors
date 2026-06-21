"""Federal Reserve Bank of Chicago — economic index products.

The Chicago Fed publishes a small fixed set of economic index families as
direct-download CSVs under chicagofed.org/-/media/publications/<product>/. Each
file is the complete historical series, overwritten in place on each release, no
auth and no pagination. The four products differ in column schema, so each is its
own publishable Delta table (one download spec + one transform spec each):

  - nfci  : National Financial Conditions Index (weekly, ending Friday, since 1971)
  - cfnai : Chicago Fed National Activity Index (monthly, since 1967)
  - mei   : Midwest Economy Index (monthly, since 1976; discontinued 2021)
  - bbki  : Brave-Butters-Kelley Indexes (monthly, since 1960; discontinued 2022)

Fetch shape: stateless full re-pull. Each file is tiny (<150KB) so we always
re-download the whole CSV and overwrite — revisions are picked up for free, no
watermark/cursor. The site 403s some default bots, so we send a browser-like
User-Agent. Date formats vary (MM/DD/YYYY for nfci/bbki, YYYY/MM for cfnai/mei)
and missing values appear as the literal string 'NaN' or empty fields; both are
normalized to NULL during parsing into typed parquet.
"""

import csv
import io
import re
from datetime import datetime

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

# Browser-like UA: the Chicago Fed CDN returns 403 to some default bot agents.
_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) subsets.io-connector/1.0"
)

# Per-product config: URL and the strptime format for the first (date) column.
# All non-date columns are parsed as floats; column names are normalized from the
# CSV header. Monthly products use YYYY/MM (mapped to the first of the month).
PRODUCTS = {
    "nfci": {
        "url": "https://www.chicagofed.org/-/media/publications/nfci/nfci-data-series-csv.csv",
        "date_fmt": "%m/%d/%Y",
    },
    "cfnai": {
        "url": "https://www.chicagofed.org/-/media/publications/cfnai/cfnai-data-series-csv.csv",
        "date_fmt": "%Y/%m",
    },
    "mei": {
        "url": "https://www.chicagofed.org/-/media/publications/mei/mei-data-series-csv.csv",
        "date_fmt": "%Y/%m",
    },
    "bbki": {
        "url": "https://www.chicagofed.org/-/media/publications/bbki/bbki-monthly-data-series-csv.csv",
        "date_fmt": "%m/%d/%Y",
    },
}


@transient_retry()
def _fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0), headers={"User-Agent": _USER_AGENT})
    resp.raise_for_status()
    return resp.text


def _normalize(name: str) -> str:
    """CSV header cell -> snake_case identifier."""
    slug = re.sub(r"[^0-9a-z]+", "_", name.strip().lower()).strip("_")
    return slug or "col"


def _to_float(cell: str):
    cell = (cell or "").strip()
    if cell == "" or cell.lower() in ("nan", "na", "n/a", "."):
        return None
    return float(cell)


def fetch_product(node_id: str) -> None:
    """Download one Chicago Fed index CSV, parse to typed parquet, overwrite."""
    asset = node_id  # the spec id IS the asset name
    product = node_id[len("chicago-fed-") :]
    cfg = PRODUCTS[product]

    text = _fetch_csv(cfg["url"])
    reader = csv.reader(io.StringIO(text))
    rows = [r for r in reader if r and any(c.strip() for c in r)]
    if not rows:
        raise AssertionError(f"{asset}: CSV had no rows")

    header = rows[0]
    # First column is the date; the rest are numeric index/subindex columns.
    value_cols = [_normalize(h) for h in header[1:]]

    dates = []
    cols = {c: [] for c in value_cols}
    for raw in rows[1:]:
        date_cell = (raw[0] if raw else "").strip()
        if not date_cell:
            continue
        d = datetime.strptime(date_cell, cfg["date_fmt"]).date()
        dates.append(d)
        for i, col in enumerate(value_cols):
            cell = raw[i + 1] if (i + 1) < len(raw) else ""
            cols[col].append(_to_float(cell))

    schema = pa.schema(
        [("date", pa.date32())] + [(c, pa.float64()) for c in value_cols]
    )
    arrays = [pa.array(dates, type=pa.date32())] + [
        pa.array(cols[c], type=pa.float64()) for c in value_cols
    ]
    table = pa.Table.from_arrays(arrays, schema=schema)
    save_raw_parquet(table, asset)


ENTITY_IDS = ["nfci", "cfnai", "mei", "bbki"]

DOWNLOAD_SPECS = [
    NodeSpec(id=f"chicago-fed-{eid}", fn=fetch_product, kind="download")
    for eid in ENTITY_IDS
]

# Raw parquet is already typed and one-row-per-date; the transform is a thin
# pass that drops any null-date rows and orders by date. 0 rows fails the node.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}" WHERE date IS NOT NULL ORDER BY date',
    )
    for s in DOWNLOAD_SPECS
]
