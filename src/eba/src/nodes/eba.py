"""European Banking Authority (EBA) connector.

The EBA exposes no machine-readable catalog/API — its statistical products are
published as downloadable files on static-HTML product pages, and the file URLs
rotate every release (they embed a release-month folder + UUID, or a per-release
numeric id). So each fetch fn re-discovers the current file URL by scraping the
relevant landing page, then downloads and parses it. Full re-pull every run
(stateless): the source has no incremental/`since` filter, and one current file
already carries the whole panel we publish.

Five published subsets, all clean tidy tables:

* risk-dashboard-kri          — EBA Risk Dashboard "Key Risk Indicators" by
                                country and EU/EEA aggregate, quarterly. The
                                single latest "Data Annex InteractiveRiskDashboard"
                                XLSX carries the full history (2014-Q4 onward) on
                                its "KRIs by country and EU" sheet, which is a
                                tidy [Period, Country, Number, Name, Ratio] table.
* te-credit-risk / -market-risk / -sovereign-exposures / -other-exposures
                              — EU-wide Transparency Exercise bank-by-bank long
                                tables (tr_cre/tr_mrk/tr_sov/tr_oth.csv) from the
                                latest exercise's Full_database. Already tidy:
                                LEI_Code, NSA, Period (YYYYMM), Item, Label,
                                template-specific breakdown dims, Amount.

Discovery is robust to URL rotation because it always parses the live listing
pages; it is NOT robust to the EBA renaming the product pages or the
"KRIs by country and EU" sheet — those would surface as a loud parse failure
(empty result -> node failure), which is the intended behaviour.
"""

import io
import csv as _csv
import re
import urllib.parse

import pyarrow as pa
import pyarrow.csv as pacsv
import openpyxl

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry

EBA_BASE = "https://www.eba.europa.eu"
RISK_DASHBOARD_PAGE = f"{EBA_BASE}/risk-and-data-analysis/risk-analysis/risk-monitoring/risk-dashboard"
TE_LANDING_PAGE = f"{EBA_BASE}/risk-and-data-analysis/risk-analysis/eu-wide-transparency-exercise"
KRI_SHEET = "KRIs by country and EU"

# Which Transparency-Exercise Full_database CSV each TE subset publishes.
TE_FILES = {
    "eba-te-credit-risk": "tr_cre.csv",
    "eba-te-market-risk": "tr_mrk.csv",
    "eba-te-sovereign-exposures": "tr_sov.csv",
    "eba-te-other-exposures": "tr_oth.csv",
}


@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 90.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(15.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _abs(href: str) -> str:
    href = href.strip()
    return href if href.startswith("http") else EBA_BASE + href


# --------------------------------------------------------------------------- #
# Risk Dashboard — Key Risk Indicators
# --------------------------------------------------------------------------- #
def _latest_risk_dashboard_annex_url() -> str:
    """Scrape the Risk Dashboard page and return the newest
    'Data Annex InteractiveRiskDashboard' XLSX URL (max year+quarter)."""
    html = _fetch_text(RISK_DASHBOARD_PAGE)
    hrefs = re.findall(r'href="([^"]*Data%20Annex%20InteractiveRiskDashboard[^"]*\.xlsx)"', html)
    if not hrefs:
        raise AssertionError("Risk Dashboard page exposed no Data Annex XLSX link")
    best = None
    for href in hrefs:
        name = urllib.parse.unquote(href)
        m = re.search(r"Q(\d)\s+(\d{4})", name)
        rank = (int(m.group(2)), int(m.group(1))) if m else (0, 0)
        if best is None or rank > best[0]:
            best = (rank, href)
    return _abs(best[1])


def fetch_risk_dashboard_kri(node_id: str) -> None:
    asset = node_id  # spec id == asset name
    content = _fetch_bytes(_latest_risk_dashboard_annex_url())
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    if KRI_SHEET not in wb.sheetnames:
        raise AssertionError(f"sheet '{KRI_SHEET}' missing; sheets={wb.sheetnames}")
    ws = wb[KRI_SHEET]

    periods, countries, codes, names, values = [], [], [], [], []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue  # header: [Period], [Country], [Number], [Name], [Ratio]
        period, country, code, name, ratio = (list(row) + [None] * 5)[:5]
        if period is None or country is None or code is None:
            continue
        periods.append(int(period))
        countries.append(str(country))
        codes.append(str(code))
        names.append(None if name is None else str(name))
        values.append(None if ratio is None else float(ratio))

    table = pa.table(
        {
            "period": pa.array(periods, pa.int32()),
            "country": pa.array(countries, pa.string()),
            "indicator_code": pa.array(codes, pa.string()),
            "indicator_name": pa.array(names, pa.string()),
            "value": pa.array(values, pa.float64()),
        }
    )
    if table.num_rows == 0:
        raise AssertionError("KRI sheet parsed to 0 rows")
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# EU-wide Transparency Exercise — bank-by-bank CSV templates
# --------------------------------------------------------------------------- #
def _latest_te_csv_url(filename: str) -> str:
    """Find the newest exercise year's Full_database URL for `filename`."""
    main = _fetch_text(TE_LANDING_PAGE)
    years = {}
    for href in re.findall(r'href="([^"]*transparency[^"]*)"', main):
        m = re.search(r"/(20\d\d)-eu-wide-transparency", href)
        if m:
            years[int(m.group(1))] = href
    if not years:
        raise AssertionError("no Transparency Exercise year pages found on landing page")

    pat = re.compile(
        r"(https://www\.eba\.europa\.eu/assets/TE\d+/Full_database/\d+/" + re.escape(filename) + r")"
    )
    for year in sorted(years, reverse=True):
        page = _fetch_text(_abs(years[year]))
        m = pat.search(page)
        if m:
            return m.group(1)
    raise AssertionError(f"no Full_database link for {filename} on any TE year page")


def _read_csv_all_string(content: bytes) -> pa.Table:
    """Read an EBA TE CSV with every column forced to string (no type inference
    surprises across a 100MB+ file); the transform casts Period/Amount."""
    header_line = content.split(b"\n", 1)[0].decode("utf-8-sig")
    cols = next(_csv.reader([header_line]))
    column_types = {c: pa.string() for c in cols}
    return pacsv.read_csv(
        io.BytesIO(content),
        convert_options=pacsv.ConvertOptions(
            column_types=column_types, strings_can_be_null=True
        ),
    )


def _fetch_te(node_id: str) -> None:
    asset = node_id
    filename = TE_FILES[node_id]
    content = _fetch_bytes(_latest_te_csv_url(filename))
    table = _read_csv_all_string(content)
    if table.num_rows == 0:
        raise AssertionError(f"{filename} parsed to 0 rows")
    save_raw_parquet(table, asset)


# Distinct top-level fns per TE spec (fn takes exactly one param = spec id).
def fetch_te_credit_risk(node_id: str) -> None:
    _fetch_te(node_id)


def fetch_te_market_risk(node_id: str) -> None:
    _fetch_te(node_id)


def fetch_te_sovereign_exposures(node_id: str) -> None:
    _fetch_te(node_id)


def fetch_te_other_exposures(node_id: str) -> None:
    _fetch_te(node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="eba-risk-dashboard-kri", fn=fetch_risk_dashboard_kri, kind="download"),
    NodeSpec(id="eba-te-credit-risk", fn=fetch_te_credit_risk, kind="download"),
    NodeSpec(id="eba-te-market-risk", fn=fetch_te_market_risk, kind="download"),
    NodeSpec(id="eba-te-sovereign-exposures", fn=fetch_te_sovereign_exposures, kind="download"),
    NodeSpec(id="eba-te-other-exposures", fn=fetch_te_other_exposures, kind="download"),
]


# --------------------------------------------------------------------------- #
# Transforms — one published Delta table per subset
# --------------------------------------------------------------------------- #
# TE files share the layout columns Footnote/Row/Column/Sheet (drop them) plus
# Period (YYYYMM string -> int) and Amount (string -> double); the rest are
# template-specific breakdown dimensions kept verbatim.
_TE_SQL = '''
    SELECT * EXCLUDE ("Footnote", "Row", "Column", "Sheet")
        REPLACE (
            CAST("Period" AS INTEGER) AS "Period",
            TRY_CAST("Amount" AS DOUBLE) AS "Amount"
        )
    FROM "{dep}"
    WHERE TRY_CAST("Amount" AS DOUBLE) IS NOT NULL
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="eba-risk-dashboard-kri-transform",
        deps=["eba-risk-dashboard-kri"],
        key=("period", "country", "indicator_code"),
        temporal="period",
        sql='''
            SELECT
                CAST(period AS INTEGER)  AS period,
                country,
                indicator_code,
                indicator_name,
                CAST(value AS DOUBLE)    AS value
            FROM "eba-risk-dashboard-kri"
            WHERE value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="eba-te-credit-risk-transform",
        deps=["eba-te-credit-risk"],
        temporal="Period",
        sql=_TE_SQL.format(dep="eba-te-credit-risk"),
    ),
    SqlNodeSpec(
        id="eba-te-market-risk-transform",
        deps=["eba-te-market-risk"],
        temporal="Period",
        sql=_TE_SQL.format(dep="eba-te-market-risk"),
    ),
    SqlNodeSpec(
        id="eba-te-sovereign-exposures-transform",
        deps=["eba-te-sovereign-exposures"],
        temporal="Period",
        sql=_TE_SQL.format(dep="eba-te-sovereign-exposures"),
    ),
    SqlNodeSpec(
        id="eba-te-other-exposures-transform",
        deps=["eba-te-other-exposures"],
        temporal="Period",
        sql=_TE_SQL.format(dep="eba-te-other-exposures"),
    ),
]
