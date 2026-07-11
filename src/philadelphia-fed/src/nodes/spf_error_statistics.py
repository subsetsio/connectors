"""SPF - forecast error statistics source workbooks."""

import io
from html.parser import HTMLParser
from urllib.parse import urljoin

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import _fetch_bytes, _fetch_html, _write

_BASE = "https://www.philadelphiafed.org"
_ERROR_PAGE_SLUGS = [
    "ngdp",
    "pgdp",
    "unemp",
    "emp",
    "indprod",
    "housing",
    "tbill",
    "bond",
    "tbond",
    "rgdp",
    "rconsum",
    "rnresin",
    "rresinv",
    "rfedgov",
    "rslgov",
    "cpi-spf",
]

_ERROR_SCHEMA = pa.schema([
    ("variable", pa.string()),
    ("date", pa.string()),
    ("series", pa.string()),
    ("horizon", pa.int64()),
    ("value", pa.float64()),
])


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.hrefs.append(href)


def _discover_error_workbooks() -> list[str]:
    urls = []
    for slug in _ERROR_PAGE_SLUGS:
        html = _fetch_html(f"{_BASE}/surveys-and-data/{slug}")
        if "<title>Error - 404</title>" in html:
            continue
        parser = _Links()
        parser.feed(html)
        for href in parser.hrefs:
            if "Data_SPF_Error_Statistics" in href and ".xls" in href:
                urls.append(urljoin(_BASE, href))
    out = sorted(set(urls))
    if len(out) < 12:
        raise AssertionError(f"SPF error statistics: discovered only {len(out)} workbooks")
    return out


def _variable_from_url(url: str) -> str:
    part = url.split("/data-files/", 1)[1].split("/", 1)[0]
    return "CPI" if part.upper() == "CPI" else part.upper()


def _series_and_horizon(col: str) -> tuple[str, int | None]:
    if "_Step" in col:
        base, step = col.rsplit("_Step", 1)
        try:
            return base, int(step)
        except ValueError:
            return base, None
    return col, None


def fetch_spf_error_statistics(node_id: str) -> None:
    import pandas as pd

    rows = []
    for url in _discover_error_workbooks():
        variable = _variable_from_url(url)
        xl = pd.ExcelFile(io.BytesIO(_fetch_bytes(url)), engine="xlrd")
        df = xl.parse(sheet_name=xl.sheet_names[0])
        df.columns = [str(c).strip() for c in df.columns]
        if "Date" not in df.columns:
            raise AssertionError(f"{variable}: no Date column in SPF error statistics workbook")
        for _, r in df.iterrows():
            date = str(r["Date"]).strip().replace(":", "-Q")
            if not date or date.lower() == "nan":
                continue
            for col in df.columns:
                if col == "Date":
                    continue
                value = r[col]
                if pd.isna(value):
                    continue
                series, horizon = _series_and_horizon(str(col))
                rows.append({
                    "variable": variable,
                    "date": date,
                    "series": series,
                    "horizon": horizon,
                    "value": float(value),
                })
    _write(rows, _ERROR_SCHEMA, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-spf-error-statistics", fn=fetch_spf_error_statistics, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-spf-error-statistics-transform",
        deps=["philadelphia-fed-spf-error-statistics"],
        sql='''
            SELECT variable, date, series, horizon, value
            FROM "philadelphia-fed-spf-error-statistics"
            WHERE value IS NOT NULL
            ORDER BY variable, date, series, horizon
        ''',
    ),
]
