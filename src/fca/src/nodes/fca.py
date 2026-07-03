"""FCA connector — node module.

Mechanism: data.gov.uk CKAN (organization 'financial-conduct-authority'). The
FCA publishes its statistical products on data.gov.uk as period-versioned CKAN
packages whose data resources are bespoke XLSX workbooks on www.fca.org.uk.

For the six rank-active products, the *latest* package's workbook is cumulative
— it carries the full historical run in one file (MLAR ships explicit
"…-long-run.xlsx" files; complaints/PSD/retirement/retail-intermediary each
carry many periods/years in the latest workbook). So each download fetches the
latest package for its family at runtime (discovered from CKAN by
metadata_modified — no hardcoded URLs or year ranges), parses the relevant
sheet(s), and writes a tidy long-format NDJSON raw. The XLSX layouts differ per
product, so all reshaping happens here in Python; the SQL transforms are thin
cast-and-project passes.

Full-corpus re-pull every run (stateless): the workbooks are small and
cumulative, so there is no watermark — re-parsing the latest file picks up
revisions for free.
"""
import io
import math
import re

import pandas as pd

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

CKAN = "https://ckan.publishing.service.gov.uk/api/3/action/"
_MONTHS = ("january|february|march|april|may|june|july|august|september|"
           "october|november|december")


# --------------------------------------------------------------------------
# CKAN discovery
# --------------------------------------------------------------------------
@transient_retry()
def _ckan_packages():
    r = get(CKAN + "package_search",
            params={"q": "organization:financial-conduct-authority", "rows": 1000},
            timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.json()["result"]["results"]


def _family(slug: str) -> str:
    """Strip the FCA prefix and trailing period/date tokens to derive the
    stable product-family key shared across release periods. Mirrors the
    grouping used by the collect stage."""
    s = re.sub(r"^fca-", "", slug)
    s = re.sub(r"-data$", "", s)
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"-(19|20)\d{2}(-\d{2})?$", "", s)
        s = re.sub(r"-q[1-4]$", "", s)
        s = re.sub(r"-h[12]$", "", s)
        s = re.sub(r"-(" + _MONTHS + r")$", "", s)
        s = re.sub(r"-(19|20)\d{2}$", "", s)
        s = re.sub(r"-\d{1,2}$", "", s)
        s = re.sub(r"-(to|and|ending|year-ending)$", "", s)
    s = re.sub(r"-data$", "", s)
    s = re.sub(r"-quarterly$", "", s)
    s = re.sub(r"^the-", "", s)
    return s.strip("-") or slug


def _latest_package(family: str) -> dict:
    members = [p for p in _ckan_packages() if _family(p["name"]) == family]
    if not members:
        raise RuntimeError(f"no CKAN packages found for family {family!r}")
    members.sort(key=lambda p: p.get("metadata_modified") or "")
    return members[-1]


def _xlsx_urls(pkg: dict, *, contains: str | None = None) -> list[str]:
    urls = []
    for res in pkg.get("resources", []):
        url = (res.get("url") or "")
        fmt = (res.get("format") or "").upper().lstrip(".")
        if fmt == "XLSX" and url.lower().endswith(".xlsx"):
            if contains is None or contains in url.lower():
                urls.append(url)
    return urls


@transient_retry()
def _get_xlsx(url: str) -> bytes:
    r = get(url, timeout=(10.0, 180.0))
    r.raise_for_status()
    return r.content


# --------------------------------------------------------------------------
# value coercion helpers
# --------------------------------------------------------------------------
def _num(v):
    """Return v as a float, or None if it isn't a finite number."""
    if v is None or isinstance(v, bool):
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(f) or math.isinf(f) else f


def _yr(v):
    f = _num(v)
    if f is None or f != int(f) or not (1990 <= f <= 2035):
        return None
    return int(f)


def _s(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    t = str(v).strip()
    return t or None


# --------------------------------------------------------------------------
# generic melters for the wide workbooks
# --------------------------------------------------------------------------
def _melt_quarterly(df: pd.DataFrame, sheet: str) -> list[dict]:
    """MLAR layout: a year-header row (a year per 4-col quarter block), a
    quarter row beneath it, metric label in col 2, unit in col 3, quarterly
    values from col 4. Emits one row per (metric, unit, year, quarter)."""
    year_row = None
    for i in range(min(30, len(df))):
        if sum(1 for c in range(df.shape[1]) if _yr(df.iat[i, c]) is not None) >= 3:
            year_row = i
            break
    if year_row is None or year_row + 1 >= len(df):
        return []
    qrow = year_row + 1
    colmap = {}
    cur_year = None
    for c in range(df.shape[1]):
        y = _yr(df.iat[year_row, c])
        if y is not None:
            cur_year = y
        q = _s(df.iat[qrow, c])
        if cur_year is not None and q and re.fullmatch(r"Q[1-4]", q):
            colmap[c] = (cur_year, q)
    if not colmap:
        return []

    rows = []
    sub_ref = None
    for i in range(qrow + 1, len(df)):
        ref = _s(df.iat[i, 0]) if df.shape[1] > 0 else None
        if ref and len(ref) <= 3:
            sub_ref = ref
        label = _s(df.iat[i, 2]) if df.shape[1] > 2 else None
        unit = _s(df.iat[i, 3]) if df.shape[1] > 3 else None
        if not label:
            continue
        for c, (yr, q) in colmap.items():
            v = _num(df.iat[i, c])
            if v is not None:
                rows.append({
                    "table_sheet": sheet, "sub_table_ref": sub_ref,
                    "metric": label, "unit": unit,
                    "year": yr, "quarter": q, "value": v,
                })
    return rows


def _melt_year_blocks(df: pd.DataFrame, section: str) -> list[dict]:
    """Retail-intermediary layout: stacked tables, each headed by a 'Year'
    row whose later columns name metrics, followed by one row per year."""
    rows = []
    table_title = None
    i = 0
    n = len(df)
    while i < n:
        c1 = _s(df.iat[i, 1]) if df.shape[1] > 1 else None
        if c1 and c1.lower().startswith("table"):
            table_title = c1
        if c1 == "Year":
            metrics = {c: _s(df.iat[i, c]) for c in range(2, df.shape[1])
                       if _s(df.iat[i, c])}
            j = i + 1
            while j < n:
                yr = _yr(df.iat[j, 1]) if df.shape[1] > 1 else None
                if yr is None:
                    break
                for c, m in metrics.items():
                    v = _num(df.iat[j, c])
                    if v is not None:
                        rows.append({"section": section, "table_title": table_title,
                                     "year": yr, "metric": m, "value": v})
                j += 1
            i = max(j, i + 1)
            continue
        i += 1
    return rows


_PERIOD_RE = re.compile(r"[A-Z][a-z]{2}\s+\d{4}\s*-\s*[A-Z][a-z]{2}\s+\d{4}")


def _melt_period_blocks(df: pd.DataFrame, sheet: str) -> list[dict]:
    """Retirement-income layout: stacked tables; each table has a period-header
    row ('Apr 2018 - Sep 2018' at each block start), a metric row beneath it,
    then one row per breakdown label in col 1."""
    rows = []
    table_title = None
    i = 0
    n = len(df)
    while i < n:
        c1 = _s(df.iat[i, 1]) if df.shape[1] > 1 else None
        if c1 and c1.lower().startswith("table"):
            table_title = c1

        period_hits = sum(1 for c in range(df.shape[1])
                          if _s(df.iat[i, c]) and _PERIOD_RE.search(_s(df.iat[i, c])))
        if period_hits >= 2 and i + 1 < n:
            colperiod = {}
            cur = None
            for c in range(df.shape[1]):
                v = _s(df.iat[i, c])
                if v:
                    m = _PERIOD_RE.search(v)
                    cur = m.group(0) if m else None
                if cur is not None and c >= 2:
                    colperiod[c] = cur
            mrow = i + 1
            colmetric = {c: _s(df.iat[mrow, c]) for c in colperiod
                         if _s(df.iat[mrow, c])}
            j = mrow + 1
            while j < n:
                lbl = _s(df.iat[j, 1]) if df.shape[1] > 1 else None
                if lbl and lbl.lower().startswith("table"):
                    break
                if sum(1 for c in range(df.shape[1])
                       if _s(df.iat[j, c]) and _PERIOD_RE.search(_s(df.iat[j, c]))) >= 2:
                    break
                if lbl:
                    for c, per in colperiod.items():
                        metric = colmetric.get(c)
                        v = _num(df.iat[j, c])
                        if metric and v is not None:
                            rows.append({"table_title": table_title, "row_label": lbl,
                                         "period": per, "metric": metric, "value": v})
                j += 1
            i = max(j, i + 1)
            continue
        i += 1
    return rows


# --------------------------------------------------------------------------
# fetch functions — one per rank-active product
# --------------------------------------------------------------------------
def fetch_firm_complaints(node_id: str) -> None:
    """Aggregate complaints — three tidy long sheets unioned. The latest
    aggregate workbook is cumulative across semesters."""
    pkg = _latest_package("firm-complaints")
    urls = _xlsx_urls(pkg, contains="aggregate")
    if not urls:
        raise RuntimeError(f"no aggregate complaints XLSX in package {pkg['name']!r}")
    xl = pd.ExcelFile(io.BytesIO(_get_xlsx(urls[0])))

    rows = []
    specs = [
        ("Firm Type", "firm_type", 1, 2, 3, None),
        ("Product Group", "product_group", 1, 2, 3, None),
        ("Product Specific", "product_specific", 1, 3, None, 2),
    ]
    for sheet, breakdown, cat_c, vtype_c, var_c, prod_c in specs:
        if sheet not in xl.sheet_names:
            continue
        df = xl.parse(sheet, header=0, dtype=object)
        vals = df.values
        for r in vals:
            sem = _s(r[0]) if len(r) > 0 else None
            vol = _num(r[4]) if len(r) > 4 else None
            if not sem or vol is None:
                continue
            rows.append({
                "semester": sem,
                "breakdown_type": breakdown,
                "category": _s(r[cat_c]),
                "product": _s(r[prod_c]) if prod_c is not None else None,
                "variable_type": _s(r[vtype_c]),
                "variable": _s(r[var_c]) if var_c is not None else None,
                "volume": vol,
            })
    save_raw_ndjson(rows, node_id)


def fetch_product_sales(node_id: str) -> None:
    """Retail Investments Product Sales Data — clean quarterly long sheet,
    cumulative across quarters in the latest annual workbook."""
    pkg = _latest_package("product-sales")
    urls = _xlsx_urls(pkg, contains="retail-investments")
    if not urls:
        raise RuntimeError(f"no retail-investments PSD XLSX in package {pkg['name']!r}")
    df = pd.read_excel(io.BytesIO(_get_xlsx(urls[0])), header=0, dtype=object)
    vals = df.values
    rows = []
    for r in vals:
        period = _s(r[3]) if len(r) > 3 else None
        sales = _num(r[4]) if len(r) > 4 else None
        if not period or sales is None:
            continue
        rows.append({
            "grouped_by": _s(r[0]),
            "category": _s(r[1]),
            "subcategory": _s(r[2]),
            "period": period,
            "no_of_sales": sales,
        })
    save_raw_ndjson(rows, node_id)


def fetch_general_insurance_value_measures(node_id: str) -> None:
    """GI value measures — firm-level 'Firms' sheet (one row per
    firm × product × year, with banded metrics)."""
    pkg = _latest_package("general-insurance-value-measures")
    urls = _xlsx_urls(pkg)
    if not urls:
        raise RuntimeError(f"no XLSX in package {pkg['name']!r}")
    xl = pd.ExcelFile(io.BytesIO(_get_xlsx(urls[0])))
    sheet = next((s for s in xl.sheet_names if s.strip().lower() == "firms"), None)
    if sheet is None:
        raise RuntimeError(f"no 'Firms' sheet in {pkg['name']!r}: {xl.sheet_names}")
    df = xl.parse(sheet, header=None, dtype=object)

    hdr = None
    for i in range(len(df)):
        if _s(df.iat[i, 0]) == "Firm Name":
            hdr = i
            break
    if hdr is None:
        raise RuntimeError("no 'Firm Name' header row in GI Firms sheet")

    rows = []
    for i in range(hdr + 1, len(df)):
        firm = _s(df.iat[i, 0])
        if not firm:
            continue
        rows.append({
            "firm_name": firm,
            "product_category": _s(df.iat[i, 1]) if df.shape[1] > 1 else None,
            "year": _yr(df.iat[i, 2]) if df.shape[1] > 2 else None,
            "band_claims_frequency": _s(df.iat[i, 3]) if df.shape[1] > 3 else None,
            "band_claims_acceptance_rate": _s(df.iat[i, 4]) if df.shape[1] > 4 else None,
            "band_average_claims_payout": _s(df.iat[i, 5]) if df.shape[1] > 5 else None,
            "band_claims_complaints_pct": _s(df.iat[i, 6]) if df.shape[1] > 6 else None,
        })
    save_raw_ndjson(rows, node_id)


def fetch_mortgage_lending_statistics(node_id: str) -> None:
    """MLAR — the cumulative long-run summary and detailed workbooks, melted
    from their quarterly wide layout into long (metric, year, quarter, value)."""
    pkg = _latest_package("mortgage-lending-statistics")
    urls = _xlsx_urls(pkg)
    if not urls:
        raise RuntimeError(f"no XLSX in package {pkg['name']!r}")
    rows = []
    for url in urls:
        book = "detailed" if "detailed" in url.lower() else "summary"
        xl = pd.ExcelFile(io.BytesIO(_get_xlsx(url)))
        for sheet in xl.sheet_names:
            if sheet.strip().lower() in ("notes", "summary contents", "contents"):
                continue
            df = xl.parse(sheet, header=None, dtype=object)
            for rec in _melt_quarterly(df, f"{book}:{sheet}"):
                rows.append(rec)
    if not rows:
        raise RuntimeError("MLAR melt produced no rows — layout may have changed")
    save_raw_ndjson(rows, node_id)


def fetch_retail_intermediary_market(node_id: str) -> None:
    """Retail intermediary market (RMAR) — year-keyed tables across the data
    sections, melted to long (section, table, year, metric, value)."""
    pkg = _latest_package("retail-intermediary-market")
    urls = _xlsx_urls(pkg)
    if not urls:
        raise RuntimeError(f"no XLSX in package {pkg['name']!r}")
    xl = pd.ExcelFile(io.BytesIO(_get_xlsx(urls[0])))
    rows = []
    for sheet in xl.sheet_names:
        if "section" not in sheet.lower():
            continue
        df = xl.parse(sheet, header=None, dtype=object)
        rows.extend(_melt_year_blocks(df, sheet.strip()))
    if not rows:
        raise RuntimeError("retail-intermediary melt produced no rows")
    save_raw_ndjson(rows, node_id)


def fetch_retirement_income_market(node_id: str) -> None:
    """Retirement income market (RIDR) — period-block data tables melted to
    long (table, row_label, period, metric, value)."""
    pkg = _latest_package("retirement-income-market")
    urls = _xlsx_urls(pkg)
    if not urls:
        raise RuntimeError(f"no XLSX in package {pkg['name']!r}")
    xl = pd.ExcelFile(io.BytesIO(_get_xlsx(urls[0])))
    rows = []
    for sheet in xl.sheet_names:
        if "data table" not in sheet.lower():
            continue
        df = xl.parse(sheet, header=None, dtype=object)
        rows.extend(_melt_period_blocks(df, sheet.strip()))
    if not rows:
        raise RuntimeError("retirement-income melt produced no rows")
    save_raw_ndjson(rows, node_id)


# --------------------------------------------------------------------------
# specs
# --------------------------------------------------------------------------
DOWNLOAD_SPECS = [
    NodeSpec(id="fca-firm-complaints", fn=fetch_firm_complaints, kind="download"),
    NodeSpec(id="fca-general-insurance-value-measures",
             fn=fetch_general_insurance_value_measures, kind="download"),
    NodeSpec(id="fca-mortgage-lending-statistics",
             fn=fetch_mortgage_lending_statistics, kind="download"),
    NodeSpec(id="fca-product-sales", fn=fetch_product_sales, kind="download"),
    NodeSpec(id="fca-retail-intermediary-market",
             fn=fetch_retail_intermediary_market, kind="download"),
    NodeSpec(id="fca-retirement-income-market",
             fn=fetch_retirement_income_market, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fca-firm-complaints-transform",
        deps=["fca-firm-complaints"],
        temporal="semester",
        sql='''
            SELECT semester,
                   breakdown_type,
                   category,
                   product,
                   variable_type,
                   variable,
                   CAST(volume AS DOUBLE) AS volume
            FROM "fca-firm-complaints"
            WHERE volume IS NOT NULL AND semester IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="fca-general-insurance-value-measures-transform",
        deps=["fca-general-insurance-value-measures"],
        key=("firm_name", "product_category", "year"),
        temporal="year",
        sql='''
            SELECT firm_name,
                   product_category,
                   CAST(year AS INTEGER) AS year,
                   band_claims_frequency,
                   band_claims_acceptance_rate,
                   band_average_claims_payout,
                   band_claims_complaints_pct
            FROM "fca-general-insurance-value-measures"
            WHERE firm_name IS NOT NULL AND year IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="fca-mortgage-lending-statistics-transform",
        deps=["fca-mortgage-lending-statistics"],
        temporal="year",
        sql='''
            SELECT table_sheet,
                   sub_table_ref,
                   metric,
                   unit,
                   CAST(year AS INTEGER) AS year,
                   quarter,
                   CAST(value AS DOUBLE) AS value
            FROM "fca-mortgage-lending-statistics"
            WHERE value IS NOT NULL AND metric IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="fca-product-sales-transform",
        deps=["fca-product-sales"],
        temporal="period",
        sql='''
            SELECT grouped_by,
                   category,
                   subcategory,
                   period,
                   CAST(regexp_extract(period, '(\\d{4})', 1) AS INTEGER) AS year,
                   regexp_extract(period, '^(Q[1-4])', 1) AS quarter,
                   CAST(no_of_sales AS DOUBLE) AS no_of_sales
            FROM "fca-product-sales"
            WHERE no_of_sales IS NOT NULL AND period IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="fca-retail-intermediary-market-transform",
        deps=["fca-retail-intermediary-market"],
        temporal="year",
        sql='''
            SELECT section,
                   table_title,
                   CAST(year AS INTEGER) AS year,
                   metric,
                   CAST(value AS DOUBLE) AS value
            FROM "fca-retail-intermediary-market"
            WHERE value IS NOT NULL AND year IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="fca-retirement-income-market-transform",
        deps=["fca-retirement-income-market"],
        temporal="period",
        sql='''
            SELECT table_title,
                   row_label,
                   period,
                   metric,
                   CAST(value AS DOUBLE) AS value
            FROM "fca-retirement-income-market"
            WHERE value IS NOT NULL AND row_label IS NOT NULL
        ''',
    ),
]
