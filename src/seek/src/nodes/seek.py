"""SEEK (AU) employment & salary indices.

Three published subsets, sourced from two XLSX bulk files SEEK publishes monthly:

  - job-ad-index              ← 'SEEK Job Ad Index' sheet of the Employment file
  - applications-per-ad-index ← 'SEEK Applications per Ad Index' sheet (same file)
  - advertised-salary-index   ← the single-sheet Advertised Salary file

Each file is a complete history, so the correct shape is a stateless full
re-pull every refresh (shape 1): download the whole file and overwrite. The
files are small (~0.45MB each) and expose no incremental filter.

The XLSX URLs live on a Hygraph asset CDN (graphassets.com) and the asset ids
rotate every monthly release, so they are NOT hardcoded — each fetch scrapes the
newsroom discovery page and resolves the current link by its anchor text. The
discovery page returns an empty body without a browser User-Agent, and the
Advertised Salary workbook ships a broken <dimension> (declares A1 only) plus a
dangling drawing rel, so it is read read-only with reset_dimensions().
"""

import io
import re

import openpyxl
import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    save_raw_parquet,
    transient_retry,
)

DISCOVERY_URL = "https://au.seek.com/about/news/seek-employment-data"
UA = "Mozilla/5.0 (compatible; subsets-connector/1.0)"

# Anchor text on the discovery page that precedes each download link.
EMP_ANCHOR = "Download the latest SEEK Employment data"
ASI_ANCHOR = "Download the latest SEEK Advertised Salary"

# Expected source headers per sheet — assert against drift.
JOBAD_HEADER = (
    "DATE", "COUNTRY", "STATE",
    "ADS_SA_INDEX", "ADS_TREND_INDEX",
    "ADS_SA_GROWTH_MONTH", "ADS_SA_GROWTH_PCP",
    "ADS_TREND_GROWTH_MONTH", "ADS_TREND_GROWTH_PCP",
)
APPS_HEADER = (
    "DATE", "COUNTRY", "STATE",
    "CA_SA_INDEX", "CA_TREND_INDEX",
    "CA_SA_GROWTH_MONTH", "CA_SA_GROWTH_PCP",
    "CA_TREND_GROWTH_MONTH", "CA_TREND_GROWTH_PCP",
)
ASI_HEADER = (
    "date", "country", "state", "classification",
    "salary_sa_index", "salary_sa_growth_month", "salary_sa_growth_pcp",
    "salary_trend_index", "salary_trend_growth_month", "salary_trend_growth_pcp",
)

# Output (raw) schemas — names lowercased, indices/growth as float64.
JOBAD_SCHEMA = pa.schema([
    ("date", pa.timestamp("s")),
    ("country", pa.string()),
    ("state", pa.string()),
    ("ads_sa_index", pa.float64()),
    ("ads_trend_index", pa.float64()),
    ("ads_sa_growth_month", pa.float64()),
    ("ads_sa_growth_pcp", pa.float64()),
    ("ads_trend_growth_month", pa.float64()),
    ("ads_trend_growth_pcp", pa.float64()),
])
APPS_SCHEMA = pa.schema([
    ("date", pa.timestamp("s")),
    ("country", pa.string()),
    ("state", pa.string()),
    ("ca_sa_index", pa.float64()),
    ("ca_trend_index", pa.float64()),
    ("ca_sa_growth_month", pa.float64()),
    ("ca_sa_growth_pcp", pa.float64()),
    ("ca_trend_growth_month", pa.float64()),
    ("ca_trend_growth_pcp", pa.float64()),
])
ASI_SCHEMA = pa.schema([
    ("date", pa.timestamp("s")),
    ("country", pa.string()),
    ("state", pa.string()),
    ("classification", pa.string()),
    ("salary_sa_index", pa.float64()),
    ("salary_sa_growth_month", pa.float64()),
    ("salary_sa_growth_pcp", pa.float64()),
    ("salary_trend_index", pa.float64()),
    ("salary_trend_growth_month", pa.float64()),
    ("salary_trend_growth_pcp", pa.float64()),
])


@transient_retry()
def _get(url, **kwargs):
    configure_http(headers={"User-Agent": UA})
    resp = get(url, timeout=(10.0, 180.0), **kwargs)
    resp.raise_for_status()
    return resp


def _discover_url(anchor: str) -> str:
    """Resolve the current CDN download URL by its anchor text on the page."""
    html = _get(DISCOVERY_URL).text
    i = html.find(anchor)
    if i < 0:
        raise AssertionError(
            f"discovery anchor {anchor!r} not found on {DISCOVERY_URL} "
            f"(page changed?)"
        )
    window = html[max(0, i - 600):i]
    hrefs = re.findall(r'href="(https://[^"]*graphassets\.com/[^"]+)"', window)
    if not hrefs:
        raise AssertionError(f"no graphassets href preceding anchor {anchor!r}")
    return hrefs[-1]


def _read_sheet(content: bytes, sheet: str, expected_header: tuple) -> list:
    """Return data rows (header excluded) from one sheet, tolerating a broken
    <dimension> declaration via reset_dimensions()."""
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    try:
        ws = wb[sheet]
        ws.reset_dimensions()  # ignore the declared range; scan actual cells
        rows = list(ws.iter_rows(values_only=True))
    finally:
        wb.close()
    if not rows:
        raise AssertionError(f"sheet {sheet!r} is empty")
    n = len(expected_header)
    header = tuple(
        (str(c).strip() if c is not None else "") for c in rows[0][:n]
    )
    if header != expected_header:
        raise AssertionError(
            f"header drift in {sheet!r}: {header} != {expected_header}"
        )
    return rows[1:]


def _rows_to_table(data_rows: list, schema: pa.Schema) -> pa.Table:
    ncols = len(schema)
    cols = [[] for _ in range(ncols)]
    for r in data_rows:
        cells = r[:ncols]
        if all(v is None for v in cells):
            continue  # trailing blank row
        for j in range(ncols):
            cols[j].append(cells[j] if j < len(cells) else None)
    arrays = [pa.array(cols[j], type=schema.field(j).type) for j in range(ncols)]
    table = pa.table(arrays, schema=schema)
    if table.num_rows == 0:
        raise AssertionError(f"sheet produced 0 data rows for schema {schema.names}")
    return table


def fetch_job_ad_index(node_id: str) -> None:
    content = _get(_discover_url(EMP_ANCHOR)).content
    rows = _read_sheet(content, "SEEK Job Ad Index", JOBAD_HEADER)
    save_raw_parquet(_rows_to_table(rows, JOBAD_SCHEMA), node_id)


def fetch_applications_per_ad_index(node_id: str) -> None:
    content = _get(_discover_url(EMP_ANCHOR)).content
    rows = _read_sheet(content, "SEEK Applications per Ad Index", APPS_HEADER)
    save_raw_parquet(_rows_to_table(rows, APPS_SCHEMA), node_id)


def fetch_advertised_salary_index(node_id: str) -> None:
    content = _get(_discover_url(ASI_ANCHOR)).content
    rows = _read_sheet(content, "Sheet 1", ASI_HEADER)
    save_raw_parquet(_rows_to_table(rows, ASI_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="seek-job-ad-index", fn=fetch_job_ad_index, kind="download"),
    NodeSpec(
        id="seek-applications-per-ad-index",
        fn=fetch_applications_per_ad_index,
        kind="download",
    ),
    NodeSpec(
        id="seek-advertised-salary-index",
        fn=fetch_advertised_salary_index,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="seek-job-ad-index-transform",
        deps=["seek-job-ad-index"],
        sql='''
            SELECT
                CAST(date AS DATE) AS date,
                country,
                state,
                ads_sa_index,
                ads_trend_index,
                ads_sa_growth_month,
                ads_sa_growth_pcp,
                ads_trend_growth_month,
                ads_trend_growth_pcp
            FROM "seek-job-ad-index"
            WHERE ads_sa_index IS NOT NULL OR ads_trend_index IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="seek-applications-per-ad-index-transform",
        deps=["seek-applications-per-ad-index"],
        sql='''
            SELECT
                CAST(date AS DATE) AS date,
                country,
                state,
                ca_sa_index,
                ca_trend_index,
                ca_sa_growth_month,
                ca_sa_growth_pcp,
                ca_trend_growth_month,
                ca_trend_growth_pcp
            FROM "seek-applications-per-ad-index"
            WHERE ca_sa_index IS NOT NULL OR ca_trend_index IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="seek-advertised-salary-index-transform",
        deps=["seek-advertised-salary-index"],
        sql='''
            SELECT
                CAST(date AS DATE) AS date,
                country,
                state,
                classification,
                salary_sa_index,
                salary_sa_growth_month,
                salary_sa_growth_pcp,
                salary_trend_index,
                salary_trend_growth_month,
                salary_trend_growth_pcp
            FROM "seek-advertised-salary-index"
            WHERE salary_sa_index IS NOT NULL OR salary_trend_index IS NOT NULL
        ''',
    ),
]
