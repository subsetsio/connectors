"""Robert Shiller Online Data downloads.

The source publishes small Excel workbooks with multi-row human headers and
older fixed-width HTML/pre tables. Raw output is normalized just enough to be
SQL-readable: workbooks are preserved as sheet row matrices with generic
columns and a parsed leading period where possible; repeat-sales files are
parsed to their documented four-column row shape with city as a column.
"""

from __future__ import annotations

from io import BytesIO
import re
from urllib.parse import urljoin

import pandas as pd
import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
)

SLUG = "shiller-data"
SHILLERDATA_URL = "https://shillerdata.com/"
LONG_TERM_URL = "http://www.econ.yale.edu/~shiller/data/chapt26.xlsx"
REPEAT_SALES_URLS = {
    "Atlanta": "http://www.econ.yale.edu/~shiller/data/atlanta.html",
    "Chicago": "http://www.econ.yale.edu/~shiller/data/chicago.html",
    "Dallas": "http://www.econ.yale.edu/~shiller/data/dallas.html",
    "Oakland": "http://www.econ.yale.edu/~shiller/data/oakland.html",
}
MAX_WORKBOOK_COLUMNS = 40

WORKBOOK_SCHEMA = pa.schema(
    [
        ("sheet_name", pa.string()),
        ("row_number", pa.int64()),
        ("period_value", pa.float64()),
        ("period_label", pa.string()),
    ]
    + [(f"col_{i:03d}", pa.string()) for i in range(1, MAX_WORKBOOK_COLUMNS + 1)]
)

REPEAT_SALES_SCHEMA = pa.schema(
    [
        ("city", pa.string()),
        ("row_number", pa.int64()),
        ("is_outlier", pa.bool_()),
        ("first_sale_price_raw", pa.string()),
        ("second_sale_price_raw", pa.string()),
        ("first_sale_quarter", pa.int64()),
        ("second_sale_quarter", pa.int64()),
    ]
)


def _download(url: str):
    response = get(url, timeout=(10.0, 120.0))
    response.raise_for_status()
    return response


def _shillerdata_file_url(filename_pattern: str) -> str:
    html = _download(SHILLERDATA_URL).text
    for href in re.findall(r'href="([^"]+)"', html):
        if re.search(filename_pattern, href, flags=re.IGNORECASE):
            return urljoin(SHILLERDATA_URL, href.replace("&amp;", "&"))
    raise RuntimeError(f"could not find download link matching {filename_pattern!r}")


def _cell_to_string(value) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    return text or None


def _period_from_first_cell(value) -> tuple[float | None, str | None]:
    if pd.isna(value):
        return None, None
    if isinstance(value, int | float) and 1000 <= float(value) <= 3000:
        return float(value), str(value)
    text = str(value).strip()
    if re.fullmatch(r"\d{4}(?:\.\d{1,2})?", text):
        return float(text), text
    return None, text or None


def _workbook_to_table(content: bytes) -> pa.Table:
    rows = []
    workbook = pd.ExcelFile(BytesIO(content))
    for sheet_name in workbook.sheet_names:
        frame = pd.read_excel(workbook, sheet_name=sheet_name, header=None)
        frame = frame.dropna(how="all")
        for row_number, (_, row) in enumerate(frame.iterrows(), start=1):
            values = [_cell_to_string(v) for v in row.tolist()[:MAX_WORKBOOK_COLUMNS]]
            values.extend([None] * (MAX_WORKBOOK_COLUMNS - len(values)))
            period_value, period_label = _period_from_first_cell(row.iloc[0])
            out = {
                "sheet_name": sheet_name,
                "row_number": row_number,
                "period_value": period_value,
                "period_label": period_label,
            }
            out.update({f"col_{i:03d}": values[i - 1] for i in range(1, MAX_WORKBOOK_COLUMNS + 1)})
            rows.append(out)
    return pa.Table.from_pylist(rows, schema=WORKBOOK_SCHEMA)


def fetch_stock_markets_cape(node_id: str) -> None:
    url = _shillerdata_file_url(r"ie_data\.xls")
    response = _download(url)
    save_raw_parquet(_workbook_to_table(response.content), node_id)
    record_source_signature(node_id, url, response=response)


def fetch_home_prices(node_id: str) -> None:
    url = _shillerdata_file_url(r"Fig3-1.*\.xls")
    response = _download(url)
    save_raw_parquet(_workbook_to_table(response.content), node_id)
    record_source_signature(node_id, url, response=response)


def fetch_long_term_market_volatility(node_id: str) -> None:
    response = _download(LONG_TERM_URL)
    save_raw_parquet(_workbook_to_table(response.content), node_id)
    record_source_signature(node_id, LONG_TERM_URL, response=response)


def _repeat_sales_rows(city: str, html: str) -> list[dict]:
    pre_match = re.search(r"<pre>(.*?)</pre>", html, flags=re.IGNORECASE | re.DOTALL)
    if not pre_match:
        raise RuntimeError(f"{city}: no <pre> block found")
    rows = []
    is_outlier = False
    row_number = 0
    for line in pre_match.group(1).splitlines():
        if "outlier" in line.lower():
            is_outlier = True
            continue
        parts = line.strip().split()
        if len(parts) != 4 or not all(re.fullmatch(r"\d+", p) for p in parts):
            continue
        row_number += 1
        rows.append(
            {
                "city": city,
                "row_number": row_number,
                "is_outlier": is_outlier,
                "first_sale_price_raw": parts[0],
                "second_sale_price_raw": parts[1],
                "first_sale_quarter": int(parts[2]),
                "second_sale_quarter": int(parts[3]),
            }
        )
    return rows


def fetch_repeat_sales_house_prices(node_id: str) -> None:
    rows = []
    for city, url in REPEAT_SALES_URLS.items():
        rows.extend(_repeat_sales_rows(city, _download(url).text))
    save_raw_parquet(pa.Table.from_pylist(rows, schema=REPEAT_SALES_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="shiller-data-long-term-market-volatility",
        fn=fetch_long_term_market_volatility,
        kind="download",
    ),
    NodeSpec(
        id="shiller-data-repeat-sales-house-prices",
        fn=fetch_repeat_sales_house_prices,
        kind="download",
    ),
    NodeSpec(
        id="shiller-data-us-home-prices",
        fn=fetch_home_prices,
        kind="download",
    ),
    NodeSpec(
        id="shiller-data-us-stock-markets-cape",
        fn=fetch_stock_markets_cape,
        kind="download",
    ),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="shiller-data-long-term-market-volatility",
        description="Static workbook observed via Last-Modified at the Yale data URL.",
        check=lambda aid: source_unchanged(aid, LONG_TERM_URL)
        and raw_asset_exists(aid, "parquet"),
    ),
]
