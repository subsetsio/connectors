"""Major Foreign Holders of U.S. Treasury Securities (MFH).

The flagship country x month series, merged from three wide-matrix files:
slt_table5 (recent ~13 months), mfhhis01 (by-country history back to ~2000),
and fht_1939-1999 (pre-2000 aggregate total only). Output is long form. The
transform is a thin DuckDB cast (YYYY-MM -> first-of-month DATE, null drop).
"""
import csv as stdlib_csv
import io
from datetime import datetime

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import BASE_RC, _clean_country, _fetch_text, _val

BASE_PUB = "https://ticdata.treasury.gov/Publish"

MONTH_MAP = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
}
# Aggregate/summary rows that are not country observations.
_SKIP_PREFIXES = ("Grand Total", "Of Which", "Of which")


def _is_summary(country: str) -> bool:
    c = country.strip()
    return (not c) or c.startswith("-") or any(c.startswith(p) for p in _SKIP_PREFIXES)


def _parse_mfh_wide(text: str) -> dict:
    """slt_table5: 'Country' header then YYYY-MM date columns (wide)."""
    lines = list(stdlib_csv.reader(io.StringIO(text), delimiter="\t"))
    hidx = None
    for i, line in enumerate(lines):
        if line and line[0].strip() == "Country":
            hidx = i
            break
    if hidx is None:
        raise ValueError("MFH current 'Country' header row not found")
    dates = [c.strip() for c in lines[hidx]]
    out = {}
    for line in lines[hidx + 1:]:
        if not line or not line[0].strip():
            continue
        country = line[0].strip()
        if _is_summary(country):
            continue
        country = _clean_country(country)
        for ci in range(1, min(len(line), len(dates))):
            d = dates[ci]
            if not d:
                continue
            v = _val(line[ci])
            if v is not None:
                out[(country, d)] = v
    return out


def _parse_mfh_hist(text: str) -> dict:
    """mfhhis01: repeating Month-row / 'Country'+Year-row blocks (wide)."""
    lines = list(stdlib_csv.reader(io.StringIO(text), delimiter="\t"))
    out = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line or line[0].strip() != "Country":
            i += 1
            continue
        year_row = line
        month_row = lines[i - 1] if i > 0 else []
        dates = []
        for ci in range(len(year_row)):
            month = month_row[ci].strip() if ci < len(month_row) else ""
            year = year_row[ci].strip()
            if month in MONTH_MAP and year.isdigit():
                dates.append((ci, f"{year}-{MONTH_MAP[month]}"))
        i += 1
        # skip the "------" separator row
        if i < len(lines) and lines[i] and any("---" in c for c in lines[i]):
            i += 1
        while i < len(lines):
            dl = lines[i]
            if not dl or not dl[0].strip():
                break
            country = dl[0].strip()
            if _is_summary(country):
                i += 1
                continue
            country = _clean_country(country)
            for ci, d in dates:
                if ci < len(dl):
                    v = _val(dl[ci])
                    if v is not None:
                        out[(country, d)] = v
            i += 1
        i += 1
    return out


def _parse_fht(text: str) -> dict:
    """fht_1939-1999: aggregate total foreign holdings only (CSV, dd-Mon-YYYY)."""
    out = {}
    for line in stdlib_csv.reader(io.StringIO(text)):
        if len(line) < 2 or not line[0].strip():
            continue
        raw = line[0].strip()
        if raw.startswith("-") or raw == "Date":
            continue
        try:
            dt = datetime.strptime(raw, "%d-%b-%Y")
        except ValueError:
            continue
        v = _val(line[1])
        if v is not None:
            out[("Total Foreign Holdings", dt.strftime("%Y-%m"))] = v
    return out


def fetch_mfh(node_id: str) -> None:
    """Fetch + merge the three MFH files into one long-format holdings parquet."""
    asset = node_id
    # Order matters: aggregate (oldest) -> historical -> current; later (more
    # recently revised) values overwrite overlapping (country, date) keys.
    merged: dict = {}
    merged.update(_parse_fht(_fetch_text(f"{BASE_PUB}/fht_1939-1999.csv")))
    merged.update(_parse_mfh_hist(_fetch_text(f"{BASE_PUB}/mfhhis01.txt")))
    merged.update(_parse_mfh_wide(_fetch_text(f"{BASE_RC}/slt_table5.txt")))
    if not merged:
        raise ValueError(f"{asset}: parsed 0 MFH data points")
    records = [
        {"country": c, "date": d, "holdings_billions": v}
        for (c, d), v in merged.items()
    ]
    records.sort(key=lambda r: (r["date"], r["country"]))
    schema = pa.schema([
        ("country", pa.string()),
        ("date", pa.string()),
        ("holdings_billions", pa.float64()),
    ])
    table = pa.Table.from_pylist(records, schema=schema)
    save_raw_parquet(table, asset)
