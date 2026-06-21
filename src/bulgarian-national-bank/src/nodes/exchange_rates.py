"""BNB official daily foreign-exchange rates.

The StERForeignCurrencies endpoint serves a ``<ROWSET>`` XML of daily rates; the
period search is capped at a 3-month window per request but accepts all
currencies at once, so a full re-pull is ~one request per calendar quarter.
History starts 2000-01-01: the BNB series goes back to 1991 but the lev was
redenominated 1000:1 on 1999-07-05, so pre-2000 values are in old lev and would
put a 1000x discontinuity in the ``rate_bgn`` column. We publish the continuous
modern series only.

Stateless full re-pull each run — the source returns full history every time.
"""

import time
import xml.etree.ElementTree as ET
from datetime import date
from urllib.parse import quote

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import BASE, PREFIX, get_bytes, xml_root

FX_PAGE = "StExternalSector/StExchangeRates/StERForeignCurrencies/index.htm"
# every currency/metal the BNB has ever quoted (from the period-search form)
FX_CURRENCIES = (
    "ATS,AUD,BEF,BRL,CAD,CHF,CNY,CYP,CZK,DEM,DKK,EEK,ESP,EUR,FIM,FRF,GBP,GRD,"
    "HKD,HRK,HUF,IDR,IEP,ILS,INR,IRP,ISK,ITL,JPY,KRW,KWD,LTL,LVL,MTL,MXN,MYR,"
    "NLG,NOK,NZD,PHP,PLN,PTE,ROL,RON,RUB,SEK,SGD,SIT,SKK,THB,TRL,TRY,USD,XAG,"
    "XAU,XEU,XPT,YUG,ZAR"
)
FX_START_YEAR = 2000  # post-redenomination; see module docstring


_FX_SCHEMA = pa.schema([
    ("date", pa.string()),            # ISO yyyy-mm-dd
    ("currency_code", pa.string()),
    ("currency_name", pa.string()),
    ("ratio", pa.float64()),
    ("rate_bgn", pa.float64()),       # levs per `ratio` units of currency
    ("reverse_rate", pa.float64()),   # currency per 1 BGN
    ("gold", pa.int64()),
])


def _quarters(start_year: int):
    today = date.today()
    for year in range(start_year, today.year + 1):
        for q in range(4):
            m1 = q * 3 + 1
            m2 = m1 + 2
            if date(year, m1, 1) > today:
                return
            d2 = 31 if m2 in (1, 3, 5, 7, 8, 10, 12) else (30 if m2 != 2 else 29)
            yield (year, m1, 1, year, m2, d2)


def _text(elem, tag):
    c = elem.find(tag)
    return c.text if c is not None and c.text is not None else None


def _to_float(v):
    if v is None:
        return None
    try:
        return float(str(v).replace(",", "").strip())
    except ValueError:
        return None


def _fetch_fx_window(y1, m1, d1, y2, m2, d2):
    url = (
        f"{BASE}/{FX_PAGE}?download=csv&search=true&downloadOper=true"
        f"&group1=second&periodStartDays={d1:02d}&periodStartMonths={m1:02d}"
        f"&periodStartYear={y1}&periodEndDays={d2:02d}&periodEndMonths={m2:02d}"
        f"&periodEndYear={y2}&valutes={quote(FX_CURRENCIES)}"
        f"&showChart=false&lang=EN"
    )
    content = get_bytes(url)
    try:
        root = xml_root(content)
    except ET.ParseError:
        return []  # empty windows return a non-XML stub
    rows = []
    for row in root.iter("ROW"):
        d = _text(row, "CURR_DATE")
        code = _text(row, "CODE")
        if not d or not code or d == "Date" or code == "Code":
            continue  # header row inside the ROWSET
        parts = d.split(".")
        if len(parts) != 3:
            continue
        iso = f"{parts[2]}-{parts[1]}-{parts[0]}"
        rows.append({
            "date": iso,
            "currency_code": code.strip(),
            "currency_name": (_text(row, "NAME_") or "").strip(),
            "ratio": _to_float(_text(row, "RATIO")),
            "rate_bgn": _to_float(_text(row, "RATE")),
            "reverse_rate": _to_float(_text(row, "REVERSERATE")),
            "gold": int(_to_float(_text(row, "GOLD")) or 0),
        })
    return rows


def fetch_exchange_rates(node_id: str) -> None:
    asset = node_id
    rows = []
    for window in _quarters(FX_START_YEAR):
        rows.extend(_fetch_fx_window(*window))
        time.sleep(0.2)
    if not rows:
        raise AssertionError(f"{asset}: fetched 0 exchange-rate observations")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_FX_SCHEMA), asset)


_FX_ID = f"{PREFIX}exchange-rates"

_FX_SQL = f'''
    SELECT
        CAST(date AS DATE)                       AS date,
        currency_code,
        currency_name,
        ratio,
        rate_bgn,
        reverse_rate,
        rate_bgn / NULLIF(ratio, 0)              AS rate_bgn_per_unit,
        currency_code IN ('XAU', 'XAG', 'XPT', 'XPD') AS is_metal
    FROM (
        SELECT *, row_number() OVER (
            PARTITION BY date, currency_code ORDER BY rate_bgn
        ) AS rn
        FROM "{_FX_ID}"
    )
    WHERE rn = 1 AND rate_bgn IS NOT NULL
'''


DOWNLOAD_SPECS = [
    NodeSpec(id=_FX_ID, fn=fetch_exchange_rates, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{_FX_ID}-transform", deps=[_FX_ID], sql=_FX_SQL),
]
