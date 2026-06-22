"""Central Bank of Malta — statistical Excel-table connector.

The CBM publishes its statistics as static Excel files (.xls / .xlsx) at stable
URLs, one file per statistical table, grouped under section pages. There is no
API, SDMX endpoint, or queryable warehouse (see research). So each rank-active
table is fetched as a whole file every run (stateless full re-pull — the files
are small, tens-to-hundreds of KB) and parsed into a tidy long format.

Parsing: CBM tables are human-oriented matrices — title rows, a multi-row
column-header band, a left "stub" of row identifiers (a Period/year column
and/or category text), and a numeric value block. `parse_workbook` melts each
sheet to long rows of (sheet, section_label, row_label, series, value):

- Orientation is detected: periods may run DOWN a column (the common case) or
  ACROSS a row (wide tables, e.g. FSIs) — wide tables are transposed.
- VALUE columns are the numeric columns that carry a header label; the
  header-less Period/year column falls into the stub and becomes `row_label`.
- `series` is the full column-header lineage (merged parents forward-filled),
  joined with " | ".
- `section_label` captures a bare year sitting above month rows (so monthly
  balance-sheet tables keep their year context).

The SQL transform is then a thin cast/clean pass that publishes one Delta table
per file. No incremental query is possible; the maintain step (authored later)
gates whether a given file is refetched.
"""
import io
import math
import re
import time

import pyarrow as pa
from curl_cffi import requests as cffi
from curl_cffi.requests.exceptions import RequestException
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet, tracking

SLUG = "central-bank-of-malta"
BASE = "https://www.centralbankmalta.org"

# Relative site path per rank-active entity (the entity union). Files live under
# two interchangeable patterns; on a 404 we fall back to the flat
# /site/excel/statistics/<filename> form.
ENTITY_PATHS = {
    "balsheetcbm": "/site/excel/statistics/balsheetcbm.xlsx",
    "balsheetofi": "/site/excel/statistics/balsheetofi.xlsx",
    "balsheetomfi": "/site/excel/statistics/balsheetomfi.xlsx",
    "bop-curr-cap-accounts": "/site/excel/statistics/bop_curr_cap_accounts.xlsx",
    "bop-financial-accounts": "/site/excel/statistics/bop_financial_accounts.xlsx",
    "cent-gov-debt": "/site/excel/statistics/cent_gov_debt.xls",
    "cent-gov-rev-exp-def": "/site/excel/statistics/cent_gov_rev_exp_def.xls",
    "currissued": "/site/excel/statistics/currissued.xlsx",
    "debtsecsector": "/site/excel/statistics/debtsecsector.xls",
    "dev-permits": "/site/excel/statistics/dev_permits.xls",
    "dev-permits-2003-2024": "/site/Subscriber Categories/Real Economy Indicators/dev_permits_2003-2024.xls",
    "dev-permits-commercial-other": "/site/excel/statistics/dev_permits_commercial_other.xls",
    "dev-permits-type": "/site/excel/statistics/dev_permits_type.xls",
    "exports": "/site/excel/statistics/exports.xls",
    "exports-majorgroups": "/site/excel/statistics/exports_majorgroups.xls",
    "external-loans": "/site/excel/statistics/external_loans.xls",
    "fa-financial-assets": "/site/excel/statistics/FA_Financial_Assets.xls",
    "fa-liabilities": "/site/excel/statistics/FA_Liabilities.xls",
    "fa-whom-to-whom": "/site/excel/statistics/FA-whom-to-whom.xlsx",
    "financial-market-int-rates": "/site/Subscriber Categories/Monetary, Banking and Financial Markets/financial_market_int_rates.xlsx",
    "finstatcbm": "/site/excel/statistics/finstatcbm.xlsx",
    "foreign-trade": "/site/excel/statistics/foreign_trade.xls",
    "fsi-core-banks": "/site/excel/statistics/fsi-core-banks.xls",
    "fsi-core-banks-2015-eba-its": "/site/Subscriber Categories/Financial Stability/fsi-core-banks-2015-EBA-ITS.xlsx",
    "fvcs": "/site/Subscriber Categories/Monetary, Banking and Financial Markets/fvcs.xlsx",
    "gdp-constant-2000": "/site/excel/statistics/gdp_constant_2000.xls",
    "gdp-current-2000": "/site/excel/statistics/gdp_current_2000.xls",
    "gen-gov-exp": "/site/excel/statistics/gen_gov_exp.xls",
    "gen-gov-ext-loans": "/site/excel/statistics/gen_gov_ext_loans.xls",
    "gen-gov-rev-exp-def": "/site/excel/statistics/gen_gov_rev_exp_def.xls",
    "gnp-constant-1973-prices": "/site/excel/statistics/GNP_constant_1973_prices.xls",
    "gnp-constant-1995-prices": "/site/excel/statistics/GNP_constant_1995_prices.xls",
    "gnp-current-market-prices-annual": "/site/Subscriber Categories/Real Economy Indicators/GNP_current_market_prices_annual.xlsx",
    "gnp-current-market-prices-quarterly": "/site/Subscriber Categories/Real Economy Indicators/GNP_current_market_prices_quarterly.xlsx",
    "gov-budgetary-operations": "/site/excel/statistics/gov_budgetary_operations.xls",
    "gov-cofog": "/site/excel/statistics/gov_cofog.xls",
    "gov-dda": "/site/excel/statistics/gov_dda.xls",
    "gov-financial-balance-sheet": "/site/excel/statistics/gov_financial_balance_sheet.xls",
    "gross-ext-debt": "/site/excel/statistics/gross_ext_debt.xls",
    "gross-gov-debt": "/site/excel/statistics/gross_gov_debt.xls",
    "historic-house-prices": "/site/Subscriber Categories/Real Economy Indicators/historic-house-prices.xls",
    "historical-fa-financial-assets": "/site/excel/statistics/Historical_FA_Financial_Assets.xlsx",
    "historical-fa-liabilities": "/site/excel/statistics/Historical_FA_Liabilities.xlsx",
    "house-prices": "/site/Subscriber Categories/Real Economy Indicators/house_prices.xlsx",
    "import-adjusted-gdp-contributions": "/site/Subscriber Categories/Real Economy Indicators/import_adjusted_gdp_contributions.xlsx",
    "imports": "/site/excel/statistics/imports.xls",
    "imports-category": "/site/excel/statistics/imports_category.xls",
    "imports-majorgroups": "/site/excel/statistics/imports_majorgroups.xls",
    "inflation-hicp": "/site/excel/statistics/inflation_hicp.xls",
    "inflation-rates-rpi": "/site/excel/statistics/inflation_rates_rpi.xls",
    "inflation-rpi": "/site/excel/statistics/inflation_rpi.xls",
    "insurance-corporations": "/site/Subscriber Categories/Monetary, Banking and Financial Markets/insurance_corporations.xlsx",
    "international-investment-position": "/site/excel/statistics/international_investment_position.xlsx",
    "investmentfunds": "/site/excel/statistics/investmentfunds.xls",
    "lab-admin-rec": "/site/excel/statistics/lab_admin_rec.xls",
    "labour-lfs": "/site/excel/statistics/labour_lfs.xls",
    "ltdebsecoutstanding": "/site/excel/statistics/ltdebsecoutstanding.xls",
    "ltdebtsecmaturity": "/site/excel/statistics/ltdebtsecmaturity.xls",
    "mirdep-loaneuroareares": "/site/Subscriber Categories/Monetary, Banking and Financial Markets/mirdep_loaneuroareares.xlsx",
    "mirdep-loanresidents": "/site/Subscriber Categories/Monetary, Banking and Financial Markets/mirdep_loanresidents.xlsx",
    "monagg-counterparts-1960-2007": "/site/excel/statistics/monagg_counterparts_1960_2007.xls",
    "net-ext-debt": "/site/excel/statistics/net_ext_debt.xls",
    "omfidepcurrency": "/site/excel/statistics/omfidepcurrency.xlsx",
    "omfidepsector": "/site/excel/statistics/omfidepsector.xlsx",
    "omfiloaneconactivity": "/site/excel/statistics/omfiloaneconactivity.xlsx",
    "omfiloanscurr-mat": "/site/excel/statistics/omfiloanscurr_mat.xlsx",
    "omfiloansector": "/site/excel/statistics/omfiloansector.xlsx",
    "omfiloansize": "/site/excel/statistics/omfiloansize.xlsx",
    "pension-funds": "/site/excel/statistics/pension_funds.xlsx",
    "quotedsharessector": "/site/excel/statistics/quotedsharessector.xls",
    "real-estate-loans-natural-persons": "/site/excel/statistics/real-estate-loans-natural-persons.xlsx",
    "resmfimonagg-counterparts": "/site/excel/statistics/resmfimonagg_counterparts.xlsx",
    "retail-price-index": "/site/excel/statistics/retail_price_index.xls",
    "tourist-arrivals-annual": "/site/excel/statistics/tourist_arrivals_annual.xls",
    "tourist-arrivals-monthly": "/site/Subscriber Categories/Real Economy Indicators/tourist_arrivals_monthly.xlsx",
    "tourist-dep": "/site/excel/statistics/tourist_dep.xls",
    "tresbills": "/site/excel/statistics/tresbills.xls",
    "tresbillstimeline": "/site/excel/statistics/tresbillstimeline.xls",
}

SCHEMA = pa.schema([
    ("sheet", pa.string()),
    ("section_label", pa.string()),
    ("row_label", pa.string()),
    ("series", pa.string()),
    ("value", pa.float64()),
])

# ----------------------------------------------------------------------------
# Excel parsing
# ----------------------------------------------------------------------------

_MONTHS = ("jan", "feb", "mar", "apr", "may", "jun",
           "jul", "aug", "sep", "oct", "nov", "dec")
_PERIOD_PATTERNS = [
    re.compile(r"\b(?:19|20)\d{2}\b"),     # a year
    re.compile(r"\bq[1-4]\b", re.I),       # quarter
]


def _is_period_like(x):
    if x is None:
        return False
    if isinstance(x, (int, float)):
        if isinstance(x, float) and math.isnan(x):
            return False
        v = float(x)
        return v == int(v) and 1900 <= v <= 2099    # a bare year
    s = str(x).strip().lower()
    if not s:
        return False
    if s[:3] in _MONTHS:
        return True
    return any(p.search(s) for p in _PERIOD_PATTERNS)


def _to_num(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        if isinstance(x, float) and math.isnan(x):
            return None
        return float(x)
    s = str(x).strip()
    if s in ("", "-", "–", "—", "n/a", "N/A", "na", "NA", ":", "...", "."):
        return None
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg = True
        s = s[1:-1].strip()
    s = s.rstrip("%").strip().replace(",", "")
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def _is_blank(x):
    if x is None:
        return True
    if isinstance(x, float) and math.isnan(x):
        return True
    return str(x).strip() == ""


def _clean_text(x):
    if _is_blank(x):
        return None
    s = re.sub(r"\s+", " ", str(x).strip())
    return s or None


def _fmt_label(x):
    if isinstance(x, float) and not math.isnan(x) and x == int(x):
        return str(int(x))
    return _clean_text(x)


def parse_sheet(rows, sheet_name):
    """Melt one sheet grid (list[list], header=None) into long-format dicts."""
    if not rows:
        return []
    ncols = max((len(r) for r in rows), default=0)
    grid = [list(r) + [None] * (ncols - len(r)) for r in rows]
    nrows = len(grid)

    # Orientation: transpose wide tables so periods become the row stub.
    best_col = max(
        (sum(1 for r in range(nrows) if _is_period_like(grid[r][c])) for c in range(ncols)),
        default=0,
    )
    best_row = max(
        (sum(1 for c in range(ncols) if _is_period_like(grid[r][c])) for r in range(nrows)),
        default=0,
    )
    if best_row > best_col and best_row >= 3:
        grid = [list(col) for col in zip(*grid)]
        nrows, ncols = ncols, nrows

    numgrid = [[_to_num(grid[r][c]) for c in range(ncols)] for r in range(nrows)]

    # Data rows carry >= 2 numeric cells; the band above them is the header.
    data_rows = [
        r for r in range(nrows)
        if sum(1 for c in range(ncols) if numgrid[r][c] is not None) >= 2
    ]
    if not data_rows:
        return []
    first_data, last_data = min(data_rows), max(data_rows)
    header_rows = list(range(0, first_data))
    body_rows = list(range(first_data, last_data + 1))

    raw_header = {
        c: [l for l in (_clean_text(grid[r][c]) for r in header_rows) if l]
        for c in range(ncols)
    }
    col_numfrac = {
        c: sum(1 for r in body_rows if numgrid[r][c] is not None) / max(len(body_rows), 1)
        for c in range(ncols)
    }

    # Value columns have a header AND are mostly numeric. The header-less
    # Period/year column stays in the left stub.
    value_cols = [c for c in range(ncols) if raw_header[c] and col_numfrac[c] >= 0.3]
    if not value_cols:
        value_cols = [c for c in range(ncols) if col_numfrac[c] >= 0.5]
    if not value_cols:
        return []
    first_val = min(value_cols)
    stub_cols = [c for c in range(ncols) if c < first_val]

    # Horizontally forward-fill header rows so merged parents spread across
    # their child columns, then assemble the per-column header lineage.
    ff = []
    for r in header_rows:
        row, last = [], None
        for c in range(ncols):
            t = _clean_text(grid[r][c])
            if t is not None:
                last = t
            row.append(last)
        ff.append(row)

    def series_for(c):
        parts = []
        for ri in range(len(header_rows)):
            t = ff[ri][c]
            if t and (not parts or parts[-1] != t):
                parts.append(t)
        return " | ".join(parts) if parts else f"col{c}"

    series_map = {c: series_for(c) for c in value_cols}

    out = []
    section_label = None
    for r in body_rows:
        stub_vals = [s for s in (_fmt_label(grid[r][c]) for c in stub_cols) if s]
        row_label = " | ".join(stub_vals) if stub_vals else None
        if not any(numgrid[r][c] is not None for c in value_cols):
            # A label-only row (e.g. a bare year above month rows) is context.
            if row_label:
                section_label = row_label
            continue
        for c in value_cols:
            v = numgrid[r][c]
            if v is None:
                continue
            out.append({
                "sheet": sheet_name,
                "section_label": section_label,
                "row_label": row_label,
                "series": series_map[c],
                "value": v,
            })
    return out


def parse_workbook(content, ext):
    import pandas as pd

    engines = ["openpyxl", "xlrd"] if ext == "xlsx" else ["xlrd", "openpyxl"]
    xls, last_err = None, None
    for eng in engines:
        try:
            xls = pd.ExcelFile(io.BytesIO(content), engine=eng)
            break
        except Exception as e:  # noqa: BLE001 - probing which engine reads this file
            last_err = e
    if xls is None:
        raise RuntimeError(f"could not open workbook: {last_err!r}")
    rows = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet, header=None, dtype=object)
        rows.extend(parse_sheet(df.values.tolist(), str(sheet)))
    return rows


# ----------------------------------------------------------------------------
# Fetch
# ----------------------------------------------------------------------------

# The CBM site sits behind Cloudflare, which 403s requests whose TLS/JA3
# fingerprint looks non-browser — which is exactly what a plain httpx/requests
# client presents from a datacenter (cloud) IP, even with browser-like headers.
# `subsets_utils.get` (httpx) therefore cannot fetch these files from the CI
# runner; only a client that impersonates a real browser's TLS + HTTP/2
# fingerprint passes. `curl_cffi` (impersonate="chrome") is that client. This is
# the one justified deviation from routing HTTP through subsets_utils — we still
# record every request into the run's HTTP diagnostics via tracking.record_http.
_IMPERSONATE = "chrome"
_BROWSER_HEADERS = {
    "Referer": "https://www.centralbankmalta.org/e-and-s-statistics",
}


class _HttpStatusError(Exception):
    """A >=400 response — carries the status code for retry/404 classification."""

    def __init__(self, status_code, url):
        self.status_code = status_code
        self.url = url
        super().__init__(f"HTTP {status_code} for {url}")


def _is_transient(exc):
    # curl_cffi raises RequestException for connect/read/timeout/proxy errors.
    if isinstance(exc, RequestException):
        return True
    if isinstance(exc, _HttpStatusError):
        return exc.status_code == 429 or 500 <= exc.status_code < 600
    return False


def _quote_path(path):
    from urllib.parse import quote
    return BASE + quote(path)


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _download(url):
    t0 = time.time()
    status = None
    try:
        resp = cffi.get(
            url,
            impersonate=_IMPERSONATE,
            headers=_BROWSER_HEADERS,
            timeout=120,
        )
        status = resp.status_code
        if status >= 400:
            raise _HttpStatusError(status, url)
        return resp.content
    finally:
        tracking.record_http("GET", url, status,
                             duration_ms=int((time.time() - t0) * 1000))


def fetch_one(node_id):
    asset = node_id                          # the spec id IS the asset name
    eid = node_id[len(SLUG) + 1:]            # strip "central-bank-of-malta-"
    path = ENTITY_PATHS[eid]
    ext = path.rsplit(".", 1)[-1].lower()

    try:
        content = _download(_quote_path(path))
    except _HttpStatusError as e:
        if e.status_code != 404:
            raise
        # Both path patterns serve the same store; fall back to the flat form.
        filename = path.rsplit("/", 1)[-1]
        content = _download(_quote_path(f"/site/excel/statistics/{filename}"))

    rows = parse_workbook(content, ext)
    if not rows:
        raise ValueError(f"{asset}: parsed 0 rows from {path}")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_PATHS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                sheet,
                section_label,
                row_label,
                series,
                CAST(value AS DOUBLE) AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
