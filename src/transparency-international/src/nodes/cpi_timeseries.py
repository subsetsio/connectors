"""CPI timeseries — country-year scores (2012-present), long format.

One published subset parsed from the "CPI Timeseries 2012 - 2025" sheet of the
annual TI CPI workbook. Stateless full re-pull (the workbook restates the full
back-series every edition).
"""

import re

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import build_reader, download_workbook, find_header, num, as_int


def _parse_timeseries(rows_of) -> list:
    rows = rows_of("CPI Timeseries 2012 - 2025")
    h = find_header(rows, "Country / Territory")
    hdr = rows[h]
    # column-letter -> (canonical_metric, year). Header casing is inconsistent
    # across editions inside the SAME sheet (2014+ say "CPI score 2014" but
    # 2012/2013 say "CPI Score 2013"), so match case-insensitively and normalize.
    _METRIC = {"cpi score": "CPI score", "rank": "Rank",
               "sources": "Sources", "standard error": "Standard error"}
    metric_cols = {}
    for col, txt in hdr.items():
        if not txt:
            continue
        m = re.match(r"(cpi score|rank|sources|standard error)\s+(\d{4})",
                     txt.strip(), re.IGNORECASE)
        if m:
            metric_cols[col] = (_METRIC[m.group(1).lower()], int(m.group(2)))
    years = sorted({y for _, y in metric_cols.values()})
    assert years, "no year columns parsed from CPI timeseries header"

    out = []
    for r in rows[h + 1:]:
        country = (r.get("A") or "").strip()
        iso3 = (r.get("B") or "").strip()
        if not country or len(iso3) != 3:
            continue
        region = (r.get("C") or "").strip() or None
        by_year = {y: {} for y in years}
        for col, (metric, y) in metric_cols.items():
            by_year[y][metric] = r.get(col)
        for y in years:
            score = num(by_year[y].get("CPI score"))
            if score is None:
                continue
            out.append({
                "country": country,
                "iso3": iso3,
                "region": region,
                "year": y,
                "cpi_score": score,
                "rank": as_int(by_year[y].get("Rank")),
                "num_sources": as_int(by_year[y].get("Sources")),
                "standard_error": num(by_year[y].get("Standard error")),
            })
    return out


_TIMESERIES_SCHEMA = pa.schema([
    ("country", pa.string()),
    ("iso3", pa.string()),
    ("region", pa.string()),
    ("year", pa.int32()),
    ("cpi_score", pa.float64()),
    ("rank", pa.int32()),
    ("num_sources", pa.int32()),
    ("standard_error", pa.float64()),
])


def fetch_timeseries(node_id: str) -> None:
    rows = _parse_timeseries(build_reader(download_workbook()))
    assert rows, "CPI timeseries parsed to 0 rows"
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_TIMESERIES_SCHEMA), node_id)

