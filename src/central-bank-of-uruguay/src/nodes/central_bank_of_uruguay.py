"""Central Bank of Uruguay (BCU) — daily exchange rates.

Single subset: the BCU `cotizaciones` SOAP web service publishes daily buy/sell
rates (TCC/TCV) against the Uruguayan peso for every currency and accounting
unit the bank quotes. Strategy is a stateless full re-pull: enumerate the
universe of currencies once (the `awsbcumonedas` "Grupo 0 = todas" call, a
superset of the local/mesa and international groups), then walk one-year windows
from a conservative floor to today, pulling every currency's rates in a single
multi-code `awsbcucotizaciones` call per window. The service caps each query at a
one-year span ("Rango de fechas excede lo permitido"), so windows are <= 1 year;
electronic history reaches back to ~2000, earlier windows simply return empty.
~38 SOAP calls per refresh, so we re-pull the whole corpus each run (revisions
picked up for free) rather than maintaining a watermark.
"""

from datetime import date, timezone, datetime
import xml.etree.ElementTree as ET

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, post, save_raw_parquet, transient_retry

_BASE = "https://cotizaciones.bcu.gub.uy/wscotizaciones/servlet"
_EP_MONEDAS = f"{_BASE}/awsbcumonedas"
_EP_COTIZ = f"{_BASE}/awsbcucotizaciones"
_HEADERS = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": "Cotiza"}

# Grupo 0 ("todas") is the full currency universe — verified superset of grupo 1
# (local/mesa) and grupo 2 (internacional billete/cable + accounting units).
_GRUPO = 0
# BCU's electronic daily series begin ~2000; 1990 is a safe floor (earlier
# windows return "No existe cotizacion" and yield no rows). The upper bound is
# the current year, discovered at run time — never hardcoded.
_FLOOR_YEAR = 1990

SCHEMA = pa.schema([
    ("fecha", pa.string()),          # quote date, ISO yyyy-mm-dd (cast to DATE in transform)
    ("moneda", pa.int32()),          # BCU currency code
    ("nombre", pa.string()),         # currency / unit name
    ("codigo_iso", pa.string()),     # ISO-ish short code as published
    ("emisor", pa.string()),         # issuer country
    ("tcc", pa.float64()),           # tipo de cambio comprador (buy rate, UYU per unit)
    ("tcv", pa.float64()),           # tipo de cambio vendedor (sell rate, UYU per unit)
    ("arb_act", pa.float64()),       # arbitrage factor
    ("forma_arbitrar", pa.int32()),  # arbitrage form flag
])


def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


@transient_retry()
def _soap(url: str, envelope: str) -> str:
    resp = post(url, data=envelope.encode("utf-8"), headers=_HEADERS, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text


def _enumerate_currencies() -> list[int]:
    env = (
        '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:cot="Cotiza"><soapenv:Body>'
        f"<cot:wsbcumonedas.Execute><cot:Entrada><cot:Grupo>{_GRUPO}</cot:Grupo>"
        "</cot:Entrada></cot:wsbcumonedas.Execute></soapenv:Body></soapenv:Envelope>"
    )
    root = ET.fromstring(_soap(_EP_MONEDAS, env))
    codes = []
    for el in root.iter():
        if _localname(el.tag) == "Codigo" and el.text and el.text.strip().isdigit():
            codes.append(int(el.text.strip()))
    if not codes:
        raise AssertionError("awsbcumonedas returned no currency codes")
    return sorted(set(codes))


def _fetch_window(codes: list[int], desde: str, hasta: str) -> list[dict]:
    items = "".join(f"<cot:item>{c}</cot:item>" for c in codes)
    env = (
        '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:cot="Cotiza"><soapenv:Body>'
        "<cot:wsbcucotizaciones.Execute><cot:Entrada>"
        f"<cot:Moneda>{items}</cot:Moneda>"
        f"<cot:FechaDesde>{desde}</cot:FechaDesde><cot:FechaHasta>{hasta}</cot:FechaHasta>"
        f"<cot:Grupo>{_GRUPO}</cot:Grupo>"
        "</cot:Entrada></cot:wsbcucotizaciones.Execute></soapenv:Body></soapenv:Envelope>"
    )
    root = ET.fromstring(_soap(_EP_COTIZ, env))
    rows = []
    for dato in root.iter():
        if _localname(dato.tag) != "datoscotizaciones.dato":
            continue
        fields = {_localname(c.tag): (c.text.strip() if c.text else None) for c in dato}
        rows.append(fields)
    return rows


def _to_float(v):
    if v is None or v == "":
        return None
    return float(v)


def _to_int(v):
    if v is None or v == "":
        return None
    return int(float(v))


def fetch_exchange_rates(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    codes = _enumerate_currencies()
    today = datetime.now(tz=timezone.utc).date()

    raw_rows = []
    for year in range(_FLOOR_YEAR, today.year + 1):
        desde = f"{year}-01-01"
        hasta = min(date(year, 12, 31), today).isoformat()
        raw_rows.extend(_fetch_window(codes, desde, hasta))

    if not raw_rows:
        raise AssertionError("no exchange-rate rows returned across the full window range")

    table = pa.table({
        "fecha": [r.get("Fecha") for r in raw_rows],
        "moneda": [_to_int(r.get("Moneda")) for r in raw_rows],
        "nombre": [r.get("Nombre") for r in raw_rows],
        "codigo_iso": [r.get("CodigoISO") for r in raw_rows],
        "emisor": [r.get("Emisor") for r in raw_rows],
        "tcc": [_to_float(r.get("TCC")) for r in raw_rows],
        "tcv": [_to_float(r.get("TCV")) for r in raw_rows],
        "arb_act": [_to_float(r.get("ArbAct")) for r in raw_rows],
        "forma_arbitrar": [_to_int(r.get("FormaArbitrar")) for r in raw_rows],
    }, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="central-bank-of-uruguay-exchange-rates", fn=fetch_exchange_rates, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="central-bank-of-uruguay-exchange-rates-transform",
        deps=["central-bank-of-uruguay-exchange-rates"],
        sql='''
            SELECT
                CAST(fecha AS DATE)        AS date,
                moneda                     AS currency_code,
                nombre                     AS currency_name,
                codigo_iso                 AS iso_code,
                emisor                     AS issuer,
                CAST(tcc AS DOUBLE)        AS buy_rate,
                CAST(tcv AS DOUBLE)        AS sell_rate,
                CAST(arb_act AS DOUBLE)    AS arbitrage_factor,
                forma_arbitrar            AS arbitrage_form
            FROM "central-bank-of-uruguay-exchange-rates"
            WHERE fecha IS NOT NULL AND moneda IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY fecha, moneda ORDER BY tcv DESC) = 1
        ''',
    ),
]
