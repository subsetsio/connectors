"""SEEK (AU) employment & salary indices.

Three published subsets, sourced from two XLSX bulk files SEEK publishes monthly:

  - job-ad-index              ← 'SEEK Job Ad Index' sheet of the Employment file
  - applications-per-ad-index ← 'SEEK Applications per Ad Index' sheet (same file)
  - advertised-salary-index   ← the single-sheet Advertised Salary file

Each file is a complete history, so the correct shape is a stateless full
re-pull every refresh (shape 1): download the whole file and overwrite. The
files are small (~0.45MB each) and expose no incremental filter.

The XLSX URLs live on a Hygraph asset CDN (graphassets.com, an S3/CloudFront
origin) and the asset ids rotate every monthly release, so they are NOT
hardcoded. Discovery is via SEEK's *public, unauthenticated* Hygraph GraphQL
content API: query all spreadsheet assets and pick the most recently updated AU
file by filename prefix. This deliberately avoids scraping the human newsroom
page (au.seek.com), which sits behind Cloudflare bot management and returns 403
to datacenter IPs; the GraphQL host and the CDN are both open. The Advertised
Salary workbook ships a broken <dimension> (declares A1 only) plus a dangling
drawing rel, so sheets are read read-only with reset_dimensions().
"""

import io

import openpyxl
import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    post,
    save_raw_parquet,
    transient_retry,
)

# Public Hygraph content API (project id embedded in SEEK's newsroom app).
GRAPHQL_URL = (
    "https://ap-southeast-2-seek-apac.cdn.hygraph.com"
    "/content/cl583oqu74ttw01ug0g4s5hmt/master"
)
XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
UA = "Mozilla/5.0 (compatible; subsets-connector/1.0)"

# Filename prefixes distinguishing the two AU bulk files (NZ variants excluded).
EMP_PREFIX = "AU_PUBLISHED_DATASET"   # employment workbook (Job Ad + Apps/Ad)
ASI_PREFIX = "seek_asi_2"             # advertised salary; excludes seek_asi_nz_*

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


@transient_retry()
def _graphql_assets() -> list:
    """Return every spreadsheet asset (newest first) from the public Hygraph API.

    Server-side `where` filters are applied untrusted — Hygraph silently ignores
    unknown filter args — so the caller re-filters in Python.
    """
    configure_http(headers={"User-Agent": UA})
    query = (
        '{ assets(where: {mimeType: "%s"}, orderBy: updatedAt_DESC, first: 200)'
        ' { fileName url updatedAt } }' % XLSX_MIME
    )
    resp = post(GRAPHQL_URL, json={"query": query}, timeout=(10.0, 60.0))
    resp.raise_for_status()
    body = resp.json()
    if body.get("errors"):
        raise AssertionError(f"Hygraph GraphQL errors: {body['errors']}")
    assets = body.get("data", {}).get("assets") or []
    if not assets:
        raise AssertionError("Hygraph returned no spreadsheet assets")
    return assets


def _discover_url(prefix: str) -> str:
    """Latest-by-updatedAt asset URL whose filename starts with `prefix`."""
    cand = [a for a in _graphql_assets() if a["fileName"].startswith(prefix)]
    if not cand:
        raise AssertionError(
            f"no spreadsheet asset with filename prefix {prefix!r} "
            f"(SEEK renamed or stopped publishing?)"
        )
    cand.sort(key=lambda a: a["updatedAt"], reverse=True)
    return cand[0]["url"]


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
    content = _get(_discover_url(EMP_PREFIX)).content
    rows = _read_sheet(content, "SEEK Job Ad Index", JOBAD_HEADER)
    save_raw_parquet(_rows_to_table(rows, JOBAD_SCHEMA), node_id)


def fetch_applications_per_ad_index(node_id: str) -> None:
    content = _get(_discover_url(EMP_PREFIX)).content
    rows = _read_sheet(content, "SEEK Applications per Ad Index", APPS_HEADER)
    save_raw_parquet(_rows_to_table(rows, APPS_SCHEMA), node_id)


def fetch_advertised_salary_index(node_id: str) -> None:
    content = _get(_discover_url(ASI_PREFIX)).content
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
        key=("date", "country", "state"),
        temporal="date",
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
        key=("date", "country", "state"),
        temporal="date",
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
        key=("date", "country", "state", "classification"),
        temporal="date",
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
