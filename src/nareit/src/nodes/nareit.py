"""Nareit connector — FTSE Nareit U.S. Real Estate Index Series.

Source: Nareit (National Association of Real Estate Investment Trusts) publishes
the FTSE Nareit U.S. Real Estate Index Series as a fixed set of legacy .xls
files under https://www.reit.com/sites/default/files/returns/. There is no API;
each file is a stable, persistent URL overwritten in place each month.

We publish ONE subset, `nareit-monthly-returns`: a long-format monthly index
performance table covering the six headline indexes plus the equity- and
mortgage-property-sector indexes. Every index/sector is the same kind of monthly
(date, total/price/income return, index level, dividend yield) series, so the
index identity is a column, not a separate table.

Fetch strategy — stateless full re-pull (shape 1). The whole corpus is ~25 small
.xls files totalling well under 1MB and ~7000 long rows; each refresh re-fetches
every file and overwrites. There is no incremental filter (the files are
overwritten in place) and re-pulling is trivially cheap, so no state/watermark.

Two file layouts, both parsed into the same long schema:
  * MonthlyHistoricalReturns.xls — the headline file. One 'Index Data' sheet with
    six index blocks side by side (stride 7 columns): per block the columns are
    Total Return, Total Index, Price Return, Price Index, Income Return,
    Dividend Yield. Block group names live in header row 5.
  * Per-sector files (Office.xls, DataCenters.xls, ...) — one 'Index Data' sheet,
    fixed columns: Date(0), Total Return(2), Total Index(3), Price Return(5),
    Price Index(6), Income Return(8), Dividend Yield(10).

In both layouts data rows are identified by an Excel date serial in column 0
(>20000, i.e. after ~1954); header/blank rows have a string or empty cell there.
Files are BIFF8/OLE2 — parsed with xlrd (openpyxl cannot open .xls).

The annual file (AnnualReturns.xls) is intentionally NOT built: it is stale on
the source side (ends 2022) and fully redundant with this monthly table.
"""
import xlrd
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://www.reit.com/sites/default/files/returns"
HEADLINE_FILE = "MonthlyHistoricalReturns.xls"

# Per-sector files -> (display name, group). Equity then mortgage property sectors.
SECTOR_FILES = {
    "Office.xls": ("Office", "equity-sector"),
    "Industrial.xls": ("Industrial", "equity-sector"),
    "Retail.xls": ("Retail", "equity-sector"),
    "ShoppingCenters.xls": ("Shopping Centers", "equity-sector"),
    "RegionalMalls.xls": ("Regional Malls", "equity-sector"),
    "FreeStanding.xls": ("Free Standing", "equity-sector"),
    "Residential.xls": ("Residential", "equity-sector"),
    "Apartments.xls": ("Apartments", "equity-sector"),
    "ManufacturedHomes.xls": ("Manufactured Homes", "equity-sector"),
    "SingleFamilyHomes.xls": ("Single Family Homes", "equity-sector"),
    "Diversified.xls": ("Diversified", "equity-sector"),
    "HealthCare.xls": ("Health Care", "equity-sector"),
    "Lodging-Resorts.xls": ("Lodging/Resorts", "equity-sector"),
    "SelfStorage.xls": ("Self Storage", "equity-sector"),
    "Timberland.xls": ("Timberland", "equity-sector"),
    "Telecommunications.xls": ("Telecommunications", "equity-sector"),
    "DataCenters.xls": ("Data Centers", "equity-sector"),
    "Gaming.xls": ("Gaming", "equity-sector"),
    "Specialty.xls": ("Specialty", "equity-sector"),
    "CommercialFinancing.xls": ("Commercial Financing", "mortgage-sector"),
    "HomeFinancing.xls": ("Home Financing", "mortgage-sector"),
}

# Sector-file fixed column offsets (0-indexed) within the single 'Index Data' sheet.
_SEC_COLS = {
    "total_return": 2, "total_index": 3,
    "price_return": 5, "price_index": 6,
    "income_return": 8, "dividend_yield": 10,
}
# Headline blocks: per-block relative offsets from the block's group-name column.
_HL_OFFSETS = {
    "total_return": 0, "total_index": 1,
    "price_return": 2, "price_index": 3,
    "income_return": 4, "dividend_yield": 5,
}
_HL_GROUP_ROW = 5  # header row carrying the six index group names

SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("index", pa.string()),
    ("group", pa.string()),
    ("total_return", pa.float64()),
    ("total_index", pa.float64()),
    ("price_return", pa.float64()),
    ("price_index", pa.float64()),
    ("income_return", pa.float64()),
    ("dividend_yield", pa.float64()),
])


@transient_retry()
def _fetch_xls(filename: str) -> bytes:
    resp = get(f"{BASE}/{filename}", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.content


def _num(cell):
    """Excel numeric cell -> float, else None (blank string, '-', text)."""
    if isinstance(cell, (int, float)) and cell != "":
        return float(cell)
    return None


def _is_data_serial(value) -> bool:
    # Data rows carry an Excel date serial (Dec-1971 ~= 26298); header/blank
    # rows have an empty or text cell in column 0.
    return isinstance(value, float) and value > 20000


def _parse_sector(content: bytes, index_name: str, group: str) -> list[dict]:
    wb = xlrd.open_workbook(file_contents=content)
    sh = wb.sheet_by_index(0)
    rows = []
    for r in range(sh.nrows):
        v = sh.cell_value(r, 0)
        if not _is_data_serial(v):
            continue
        d = xlrd.xldate.xldate_as_datetime(v, wb.datemode).date()
        rows.append({
            "date": d,
            "index": index_name,
            "group": group,
            **{k: _num(sh.cell_value(r, c)) for k, c in _SEC_COLS.items()},
        })
    return rows


def _parse_headline(content: bytes) -> list[dict]:
    wb = xlrd.open_workbook(file_contents=content)
    sh = wb.sheet_by_name("Index Data")
    blocks = [
        (c, str(sh.cell_value(_HL_GROUP_ROW, c)).replace("TM", "").strip())
        for c in range(sh.ncols)
        if str(sh.cell_value(_HL_GROUP_ROW, c)).strip()
    ]
    if not blocks:
        raise AssertionError(
            f"{HEADLINE_FILE}: no index group names in header row {_HL_GROUP_ROW} "
            "- file layout changed"
        )
    rows = []
    for r in range(sh.nrows):
        v = sh.cell_value(r, 0)
        if not _is_data_serial(v):
            continue
        d = xlrd.xldate.xldate_as_datetime(v, wb.datemode).date()
        for col, name in blocks:
            rows.append({
                "date": d,
                "index": name,
                "group": "headline",
                **{k: _num(sh.cell_value(r, col + off))
                   for k, off in _HL_OFFSETS.items()},
            })
    return rows


def fetch_monthly_returns(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    rows = _parse_headline(_fetch_xls(HEADLINE_FILE))
    for filename, (name, group) in SECTOR_FILES.items():
        rows.extend(_parse_sector(_fetch_xls(filename), name, group))
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="nareit-monthly-returns", fn=fetch_monthly_returns, kind="download"),
]


# Thin parse-and-type pass: the raw is already long and typed, so the transform
# just drops the index-inception rows (a baseline index level of 100 with no
# return) and exposes the table. A (date, index) pair is the natural key.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nareit-monthly-returns-transform",
        deps=["nareit-monthly-returns"],
        sql='''
            SELECT
                date,
                "index",
                "group",
                total_return,
                total_index,
                price_return,
                price_index,
                income_return,
                dividend_yield
            FROM "nareit-monthly-returns"
            WHERE total_return IS NOT NULL
            ORDER BY "index", date
        ''',
    ),
]
