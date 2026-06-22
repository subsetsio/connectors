"""Banco Central del Uruguay (BCU) — official daily exchange rates.

Mechanism: the BCU SOAP cotizaciones web service
(cotizaciones.bcu.gub.uy/wscotizaciones). Two operations are used:

  * awsbcumonedas      -> enumerate the currency universe of a group
  * awsbcucotizaciones -> daily buy/sell/arbitrage rates per currency, capped
                          at a 31-day window per request

We publish ONE subset, `exchange-rates`: long-format daily official rates for
group 1 (mercado de cambios / local market, ~31 currencies) vs the Uruguayan
peso, from 2000 (the earliest the service returns) to today.

Fetch shape: stateless full re-pull. The whole history is a few hundred 30-day
windows (~minutes, no auth, no cost), so we re-pull every run and overwrite —
revisions and late corrections are picked up for free, no watermark to drift.
"""

from datetime import date, timedelta
import xml.etree.ElementTree as ET

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, post, save_raw_parquet, transient_retry

_COT_URL = "https://cotizaciones.bcu.gub.uy/wscotizaciones/servlet/awsbcucotizaciones"
_MON_URL = "https://cotizaciones.bcu.gub.uy/wscotizaciones/servlet/awsbcumonedas"

# Group 1 = mercado de cambios (local market): the official UYU buy/sell rates.
_GROUP = 1
# Earliest date the service returns data for (probed: 1999 -> empty, 2000 -> data).
_SOURCE_MIN = date(2000, 1, 1)
# Server hard-caps a cotizaciones query at 31 days; stay just under it.
_WINDOW_DAYS = 30

_SCHEMA = pa.schema([
    ("fecha", pa.string()),
    ("moneda", pa.int64()),
    ("nombre", pa.string()),
    ("codigo_iso", pa.string()),
    ("emisor", pa.string()),
    ("tcc", pa.float64()),
    ("tcv", pa.float64()),
    ("arbitraje", pa.float64()),
    ("forma_arbitrar", pa.int64()),
    ("grupo", pa.int64()),
])


@transient_retry()
def _soap(url: str, action: str, inner: str) -> ET.Element:
    body = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:cot="Cotiza">'
        f"<soap:Body>{inner}</soap:Body></soap:Envelope>"
    ).encode("utf-8")
    resp = post(
        url,
        data=body,
        headers={"Content-Type": "text/xml; charset=utf-8", "SOAPAction": action},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return ET.fromstring(resp.content)


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _enumerate_currencies(grupo: int) -> list[int]:
    """Currency codes published for a group, via awsbcumonedas."""
    root = _soap(
        _MON_URL,
        "Cotizaaction/AWSBCUMONEDAS.Execute",
        "<cot:wsbcumonedas.Execute><cot:Entrada>"
        f"<cot:Grupo>{grupo}</cot:Grupo>"
        "</cot:Entrada></cot:wsbcumonedas.Execute>",
    )
    codes = []
    for el in root.iter():
        if _local(el.tag) == "Codigo" and el.text:
            codes.append(int(el.text))
    if not codes:
        raise AssertionError(f"awsbcumonedas returned no currency codes for group {grupo}")
    return codes


def _to_float(text):
    if text is None or text == "":
        return None
    return float(text)


def _fetch_window(codes: list[int], desde: date, hasta: date, grupo: int) -> list[dict]:
    """One cotizaciones call for a <=31-day window across all `codes`.

    Empty windows (weekends/holidays/before-history) come back as status 0 with
    a single nil-Fecha placeholder row — those are filtered out here.
    """
    items = "".join(f"<cot:item>{c}</cot:item>" for c in codes)
    inner = (
        "<cot:wsbcucotizaciones.Execute><cot:Entrada>"
        f"<cot:Moneda>{items}</cot:Moneda>"
        f"<cot:FechaDesde>{desde.isoformat()}</cot:FechaDesde>"
        f"<cot:FechaHasta>{hasta.isoformat()}</cot:FechaHasta>"
        f"<cot:Grupo>{grupo}</cot:Grupo>"
        "</cot:Entrada></cot:wsbcucotizaciones.Execute>"
    )
    root = _soap(_COT_URL, "Cotizaaction/AWSBCUCOTIZACIONES.Execute", inner)

    rows = []
    cur = {}
    fields = {"Fecha", "Moneda", "Nombre", "CodigoISO", "Emisor", "TCC", "TCV", "ArbAct", "FormaArbitrar"}
    for el in root.iter():
        t = _local(el.tag)
        if t not in fields:
            continue
        if t == "Fecha":
            if cur:
                rows.append(cur)
            cur = {"Fecha": el.text}
        else:
            cur[t] = el.text
    if cur:
        rows.append(cur)

    out = []
    for r in rows:
        if not r.get("Fecha"):  # nil-Fecha placeholder from an empty window
            continue
        out.append({
            "fecha": r["Fecha"],
            "moneda": int(r["Moneda"]),
            "nombre": (r.get("Nombre") or "").strip() or None,
            "codigo_iso": (r.get("CodigoISO") or "").strip() or None,
            "emisor": (r.get("Emisor") or "").strip() or None,
            "tcc": _to_float(r.get("TCC")),
            "tcv": _to_float(r.get("TCV")),
            "arbitraje": _to_float(r.get("ArbAct")),
            "forma_arbitrar": int(r["FormaArbitrar"]) if r.get("FormaArbitrar") not in (None, "") else None,
            "grupo": grupo,
        })
    return out


def fetch_exchange_rates(node_id: str) -> None:
    asset = node_id
    codes = _enumerate_currencies(_GROUP)

    today = date.today()
    all_rows = []
    start = _SOURCE_MIN
    while start <= today:
        end = min(start + timedelta(days=_WINDOW_DAYS), today)
        all_rows.extend(_fetch_window(codes, start, end, _GROUP))
        start = end + timedelta(days=1)

    if not all_rows:
        raise AssertionError("BCU cotizaciones returned no rows across the full history window")

    table = pa.Table.from_pylist(all_rows, schema=_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="banco-central-del-uruguay-exchange-rates",
        fn=fetch_exchange_rates,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="banco-central-del-uruguay-exchange-rates-transform",
        deps=["banco-central-del-uruguay-exchange-rates"],
        sql='''
            SELECT DISTINCT
                CAST(fecha AS DATE)            AS date,
                moneda                         AS currency_code,
                nombre                         AS currency_name,
                codigo_iso                     AS iso_code,
                emisor                         AS issuer,
                CAST(tcc AS DOUBLE)            AS rate_buy,
                CAST(tcv AS DOUBLE)            AS rate_sell,
                CAST(arbitraje AS DOUBLE)      AS arbitrage,
                forma_arbitrar                 AS arbitrage_form,
                grupo                          AS market_group
            FROM "banco-central-del-uruguay-exchange-rates"
            WHERE fecha IS NOT NULL
              AND tcc IS NOT NULL
        ''',
    ),
]
