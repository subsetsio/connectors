"""Port of Los Angeles statistics downloads.

The DataLA historical TEU mirror is a regular Socrata table. The Port's current
statistics pages are static, responsive HTML tables whose markup often encodes
values in row/column headers, so the download normalizes each page to a
cell-level parquet table and leaves semantic reshaping to transforms.
"""

from io import StringIO
import math
import re

import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, get, save_raw_parquet


PREFIX = "port-of-los-angeles-"

SOCRATA_URL = "https://data.lacity.org/resource/38a8-tm7u.json"

HTML_PAGES = {
    "port-of-los-angeles-automobile-statistics": "automobile-statistics",
    "port-of-los-angeles-breakbulk-statistics": "breakbulk-statistics",
    "port-of-los-angeles-container-statistics": "container-statistics",
    "port-of-los-angeles-cruise-statistics": "cruise-statistics",
    "port-of-los-angeles-facts-and-figures": "facts-and-figures",
    "port-of-los-angeles-tonnage-statistics": "tonnage-statistics",
}

HISTORICAL_SCHEMA = pa.schema(
    [
        ("year", pa.int64()),
        ("teus_in_million", pa.float64()),
    ]
)

HTML_CELL_SCHEMA = pa.schema(
    [
        ("page_slug", pa.string()),
        ("table_index", pa.int64()),
        ("row_index", pa.int64()),
        ("column_index", pa.int64()),
        ("column_name", pa.string()),
        ("column_path", pa.string()),
        ("value", pa.string()),
        ("extraction_kind", pa.string()),
    ]
)


def _clean(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    text = re.sub(r"\s+", " ", str(value).replace("\u200b", "")).strip()
    if not text or text.lower() == "nan" or text.startswith("Unnamed:"):
        return None
    return text


def _column_values(column) -> list[str]:
    if isinstance(column, tuple):
        raw_values = column
    else:
        raw_values = (column,)
    return [text for value in raw_values if (text := _clean(value))]


def _column_name(column) -> str | None:
    values = _column_values(column)
    return values[0] if values else None


def _column_path(column) -> str | None:
    values = _column_values(column)
    return " | ".join(values) if values else None


def fetch_historical_teu_statistics(node_id: str) -> None:
    resp = get(SOCRATA_URL, params={"$limit": 5000}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    rows = []
    for row in resp.json():
        rows.append(
            {
                "year": int(row["year"]),
                "teus_in_million": float(row["teus_in_million"]),
            }
        )
    table = pa.Table.from_pylist(rows, schema=HISTORICAL_SCHEMA)
    save_raw_parquet(table, node_id)


def _html_cells(page_slug: str, html: str) -> list[dict]:
    cells: list[dict] = []
    tables = pd.read_html(StringIO(html), header=None)
    for table_index, frame in enumerate(tables):
        if frame.empty:
            for column_index, column in enumerate(frame.columns):
                path = _column_path(column)
                if not path:
                    continue
                for row_index, value in enumerate(_column_values(column)):
                    cells.append(
                        {
                            "page_slug": page_slug,
                            "table_index": table_index,
                            "row_index": row_index,
                            "column_index": column_index,
                            "column_name": _column_name(column),
                            "column_path": path,
                            "value": value,
                            "extraction_kind": "column_tuple",
                        }
                    )
            continue

        reset = frame.reset_index()
        for row_index, row in reset.iterrows():
            for column_index, column in enumerate(reset.columns):
                value = _clean(row.iloc[column_index])
                path = _column_path(column)
                if value is None or path is None:
                    continue
                cells.append(
                    {
                        "page_slug": page_slug,
                        "table_index": table_index,
                        "row_index": int(row_index),
                        "column_index": int(column_index),
                        "column_name": _column_name(column),
                        "column_path": path,
                        "value": value,
                        "extraction_kind": "cell",
                    }
                )
    return cells


def fetch_statistics_page(node_id: str) -> None:
    page_slug = HTML_PAGES[node_id]
    url = f"https://portoflosangeles.org/business/statistics/{page_slug}"
    resp = get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; subsets-factory/1.0)"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    cells = _html_cells(page_slug, resp.text)
    if not cells:
        raise RuntimeError(f"{page_slug}: no table cells parsed from statistics page")
    table = pa.Table.from_pylist(cells, schema=HTML_CELL_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="port-of-los-angeles-automobile-statistics", fn=fetch_statistics_page, kind="download"),
    NodeSpec(id="port-of-los-angeles-breakbulk-statistics", fn=fetch_statistics_page, kind="download"),
    NodeSpec(id="port-of-los-angeles-container-statistics", fn=fetch_statistics_page, kind="download"),
    NodeSpec(id="port-of-los-angeles-cruise-statistics", fn=fetch_statistics_page, kind="download"),
    NodeSpec(id="port-of-los-angeles-facts-and-figures", fn=fetch_statistics_page, kind="download"),
    NodeSpec(id="port-of-los-angeles-historical-teu-statistics", fn=fetch_historical_teu_statistics, kind="download"),
    NodeSpec(id="port-of-los-angeles-tonnage-statistics", fn=fetch_statistics_page, kind="download"),
]
