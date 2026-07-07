"""Banco Central del Paraguay (BCP) — exchange-rate connector.

BCP exposes machine-readable data only through its 'cotizacion' web app
(server-rendered HTML tables under /webapps/web/cotizacion/). There is no API,
no bulk export, and no incremental filter — but the year (`anho`) path param is
a date selector, so each year/month page is an immutable historical slice. The
fetch shape is therefore a STATELESS full re-pull: iterate every year from
BCP's earliest cotizacion year (2001, verified by probing) to the current year
and re-scrape. Out-of-range years return HTTP 200 with an all-'ND' grid, which
yields no rows, so a uniform 2001..current sweep is safe for every endpoint
even though the free-market series only begins mid-2010s. Volume is small
(~400 small HTML pages total across the three nodes), so full re-pull each run
costs a few minutes and trivially picks up revisions.

Three independent download nodes, one per published subset:
  - monthly-currency-reference-rates  (monedas-mensual, ~23 currencies x month)
  - daily-usd-reference-rate          (monedas-historica, USD, daily grid)
  - daily-usd-free-market-rate        (referencial-fluctuante/anual, compra+venta)
"""

import re
from datetime import date, datetime, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://www.bcp.gov.py/webapps/web/cotizacion"
# BCP's cotizacion archive begins in 2001 (verified by probing: 2000 and
# earlier return empty grids). Upper bound is dynamic — the current year.
START_YEAR = 2001

_MONTH_COLS = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP",
               "OCT", "NOV", "DIC"]


def _years():
    return range(START_YEAR, datetime.now(timezone.utc).year + 1)


@transient_retry()
def _get_text(url, params):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _cells(tr):
    out = []
    for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S | re.I):
        c = re.sub(r"<[^>]+>", " ", c)
        c = c.replace("&nbsp;", " ")
        out.append(re.sub(r"\s+", " ", c).strip())
    return out


def _rows(html):
    return [_cells(tr) for tr in re.findall(r"<tr.*?</tr>", html, re.S | re.I)]


def _last_table(html):
    tabs = re.findall(r"<table.*?</table>", html, re.S | re.I)
    return tabs[-1] if tabs else ""


def _num(s):
    """Parse a Spanish-locale number ('4.431,00' -> 4431.0); 'ND'/blank -> None."""
    s = (s or "").strip()
    if not re.match(r"^\d[\d.]*,\d+$", s):
        return None
    return float(s.replace(".", "").replace(",", "."))


def _grid_to_daily(html, year):
    """A 'planilla del anho' grid: rows of [day, ENE..DIC] cells -> dict
    {(month, day): value} for the cells that parse as numbers."""
    out = {}
    for cells in _rows(_last_table(html)):
        if len(cells) < 13 or not cells[0].isdigit():
            continue
        day = int(cells[0])
        for mi in range(12):
            v = _num(cells[1 + mi])
            if v is not None:
                out[(mi + 1, day)] = v
    return out


def _valid_date(year, month, day):
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _month_end(year, month):
    if month == 12:
        return date(year, 12, 31)
    return date(year, month + 1, 1) - date.resolution


# --------------------------------------------------------------------------- #
# monthly-currency-reference-rates
# --------------------------------------------------------------------------- #
_MONTHLY_SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("date", pa.date32()),
    ("currency_code", pa.string()),
    ("currency_name", pa.string()),
    ("units_per_usd", pa.float64()),
    ("guaranies_per_unit", pa.float64()),
])


def fetch_monthly_currency(node_id):
    asset = node_id
    rows = []
    for year in _years():
        for month in range(1, 13):
            html = _get_text(f"{BASE}/monedas-mensual",
                             {"anho": year, "mes": month})
            for cells in _rows(html):
                # data rows look like [name, ISO_code, me/usd, guaranies/me]
                if len(cells) != 4 or not re.match(r"^[A-Z]{2,4}$", cells[1]):
                    continue
                rows.append({
                    "year": year,
                    "month": month,
                    "date": _month_end(year, month),
                    "currency_code": cells[1],
                    "currency_name": cells[0].rstrip(" *").strip(),
                    "units_per_usd": _num(cells[2]),
                    "guaranies_per_unit": _num(cells[3]),
                })
    table = pa.Table.from_pylist(rows, schema=_MONTHLY_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# daily-usd-reference-rate
# --------------------------------------------------------------------------- #
_DAILY_REF_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("guaranies_per_usd", pa.float64()),
])


def fetch_daily_usd_reference(node_id):
    asset = node_id
    rows = []
    for year in _years():
        html = _get_text(f"{BASE}/monedas-historica",
                         {"anho": year, "moneda": "USD"})
        for (month, day), value in _grid_to_daily(html, year).items():
            d = _valid_date(year, month, day)
            if d is not None:
                rows.append({"date": d, "guaranies_per_usd": value})
    table = pa.Table.from_pylist(rows, schema=_DAILY_REF_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# daily-usd-free-market-rate
# --------------------------------------------------------------------------- #
_FREE_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("compra", pa.float64()),
    ("venta", pa.float64()),
])


def fetch_daily_usd_free_market(node_id):
    asset = node_id
    rows = []
    for year in _years():
        compra = _grid_to_daily(
            _get_text(f"{BASE}/referencial-fluctuante/anual",
                      {"anho": year, "tipoOperacion": "compra"}), year)
        venta = _grid_to_daily(
            _get_text(f"{BASE}/referencial-fluctuante/anual",
                      {"anho": year, "tipoOperacion": "venta"}), year)
        for (month, day) in sorted(set(compra) | set(venta)):
            d = _valid_date(year, month, day)
            if d is not None:
                rows.append({
                    "date": d,
                    "compra": compra.get((month, day)),
                    "venta": venta.get((month, day)),
                })
    table = pa.Table.from_pylist(rows, schema=_FREE_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# Specs
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(
        id="banco-central-del-paraguay-monthly-currency-reference-rates",
        fn=fetch_monthly_currency,
        kind="download",
    ),
    NodeSpec(
        id="banco-central-del-paraguay-daily-usd-reference-rate",
        fn=fetch_daily_usd_reference,
        kind="download",
    ),
    NodeSpec(
        id="banco-central-del-paraguay-daily-usd-free-market-rate",
        fn=fetch_daily_usd_free_market,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="banco-central-del-paraguay-monthly-currency-reference-rates-transform",
        deps=["banco-central-del-paraguay-monthly-currency-reference-rates"],
        sql='''
            SELECT
                last_day(make_date(year, month, 1))  AS date,
                currency_code,
                currency_name,
                units_per_usd,
                guaranies_per_unit
            FROM "banco-central-del-paraguay-monthly-currency-reference-rates"
            WHERE units_per_usd IS NOT NULL OR guaranies_per_unit IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="banco-central-del-paraguay-daily-usd-reference-rate-transform",
        deps=["banco-central-del-paraguay-daily-usd-reference-rate"],
        sql='''
            SELECT
                CAST(date AS DATE)  AS date,
                guaranies_per_usd
            FROM "banco-central-del-paraguay-daily-usd-reference-rate"
            WHERE guaranies_per_usd IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="banco-central-del-paraguay-daily-usd-free-market-rate-transform",
        deps=["banco-central-del-paraguay-daily-usd-free-market-rate"],
        sql='''
            SELECT
                CAST(date AS DATE)  AS date,
                compra,
                venta
            FROM "banco-central-del-paraguay-daily-usd-free-market-rate"
            WHERE compra IS NOT NULL OR venta IS NOT NULL
        ''',
    ),
]
