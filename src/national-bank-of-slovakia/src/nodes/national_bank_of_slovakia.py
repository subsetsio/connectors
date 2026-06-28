"""National Bank of Slovakia (NBS) — exchange-rate connector.

Publishes NBS's "Exchange Rates of Selected Foreign Currencies against the EUR"
(ERSFC) — the bank's own monthly reference rates for ~130-150 exotic currencies
the ECB does not quote daily (AFN, ALL, DZD, ...). History reaches back to 1996.

Source surface: NBS's only first-party machine-readable endpoint is the per-period
export at https://nbs.sk/export/{lang}/exchange-rate-foreign/{YYYY-MM}/xml — one
XML document per month, no bulk/range endpoint. Building the full history means
walking the month axis (~370 requests total across 1996..now).

Scope note: NBS also republishes the ECB daily EUR reference rates at
/export/.../exchange-rate/{date}/... but that is (a) ECB data, better served by a
dedicated ECB connector from ECB's own bulk history file, and (b) ~7000 per-date
requests that nbs.sk's WAF blocks (403) once a single cloud IP exceeds a few
thousand requests in a run. So this connector ships only the monthly
selected-foreign-currency feed, whose low request volume stays under that ceiling.

Fetch shape: stateless full re-pull. ~370 monthly documents fit comfortably in one
run and in memory (~50k rows), so each refresh re-walks 1996..current month and
overwrites — revisions are picked up for free, no watermark to drift.

WAF pacing: nbs.sk fronts a rate/token-bucket WAF that 403s a client IP that bursts
(observed: ~150 requests at ~125 req/min trips it; but a slow ~10 req/min pace
sustained thousands of requests in probing). So requests are strictly sequential,
single-connection, spaced ~6s apart (~10 req/min) with a browser-like User-Agent —
the full ~370-month walk finishes in ~35 min, well under the per-IP burst ceiling
and the run budget.

The XML uses NBS's <nbsExtRateList> shape (under, quirkily, the sitemap namespace);
values carry comma thousands-separators. Some currency codes (CFA franc XOF, East
Caribbean dollar XCD, ...) appear under several country rows in one month — the
transform dedups to one row per (month, currency_code).
"""

from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    configure_http,
    transient_retry,
    save_raw_parquet,
)

BASE = "https://nbs.sk/export/en"
EARLIEST_FOREIGN_YEAR = 1996    # NBS selected-foreign-currency rates begin 1996

# Browser-like UA + a deliberate inter-request delay holding the pace near
# ~10 req/min — slow enough to stay under the WAF's burst ceiling that 403s
# faster clients (see module docstring).
_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
_REQUEST_DELAY_S = 6.0

FOREIGN_SCHEMA = pa.schema([
    ("valid_from", pa.date32()),
    ("country", pa.string()),
    ("currency_code", pa.string()),
    ("currency_name", pa.string()),
    ("value", pa.float64()),
])

_FOREIGN_NS = {"n": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def _today() -> date:
    return datetime.now(tz=timezone.utc).date()


@transient_retry()
def _http_get(url: str):
    resp = get(url, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp


def _to_float(token: str) -> float:
    # NBS uses '.' as decimal and ',' as a thousands separator (e.g. "16,872.43").
    return float(token.replace(",", ""))


def _parse_foreign_xml(content: bytes) -> list[dict]:
    root = ET.fromstring(content)
    vf = root.findtext("n:validFrom", namespaces=_FOREIGN_NS)
    valid_from = date.fromisoformat(vf) if vf else None
    rows = []
    for rt in root.iterfind(".//n:rate", _FOREIGN_NS):
        code = rt.findtext("n:ccyCode", namespaces=_FOREIGN_NS)
        val = rt.findtext("n:value", namespaces=_FOREIGN_NS)
        if not code or not val or not val.strip():
            continue
        rows.append({
            "valid_from": valid_from,
            "country": rt.findtext("n:country", namespaces=_FOREIGN_NS),
            "currency_code": code,
            "currency_name": rt.findtext("n:currency", namespaces=_FOREIGN_NS),
            "value": _to_float(val),
        })
    return rows


def fetch_exchange_rate_foreign_monthly(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    configure_http(headers={"User-Agent": _USER_AGENT})

    today = _today()
    rows: list[dict] = []
    for year in range(EARLIEST_FOREIGN_YEAR, today.year + 1):
        last_month = today.month if year == today.year else 12
        for month in range(1, last_month + 1):
            resp = _http_get(f"{BASE}/exchange-rate-foreign/{year}-{month:02d}/xml")
            if resp.content.strip():
                rows.extend(_parse_foreign_xml(resp.content))
            time.sleep(_REQUEST_DELAY_S)

    table = pa.Table.from_pylist(rows, schema=FOREIGN_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="national-bank-of-slovakia-exchange-rate-foreign-monthly",
        fn=fetch_exchange_rate_foreign_monthly,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="national-bank-of-slovakia-exchange-rate-foreign-monthly-transform",
        deps=["national-bank-of-slovakia-exchange-rate-foreign-monthly"],
        sql='''
            SELECT valid_from, currency_code, country, currency_name, value
            FROM (
                SELECT
                    CAST(valid_from AS DATE) AS valid_from,
                    currency_code,
                    country,
                    currency_name,
                    CAST(value AS DOUBLE)    AS value,
                    row_number() OVER (
                        PARTITION BY valid_from, currency_code ORDER BY value DESC
                    ) AS rn
                FROM "national-bank-of-slovakia-exchange-rate-foreign-monthly"
                WHERE value IS NOT NULL
            )
            WHERE rn = 1
        ''',
    ),
]
