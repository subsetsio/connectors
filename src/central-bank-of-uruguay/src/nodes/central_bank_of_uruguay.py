"""Central Bank of Uruguay (BCU) — daily exchange rates.

Single subset: the BCU `cotizaciones` SOAP web service publishes daily buy/sell
rates (TCC/TCV) against the Uruguayan peso for every currency and accounting
unit the bank quotes. Strategy is a stateless full re-pull: enumerate the
universe of currencies once (the `awsbcumonedas` "Grupo 0 = todas" call, a
superset of the local/mesa and international groups), then pull every currency's
rates over the full history in a single multi-code `awsbcucotizaciones` call per
month-window. The service caps each query's date span as a function of how many
currencies are requested ("Rango de fechas excede lo permitido") — with the full
~40-code set roughly two months is the ceiling, so we chunk by calendar month
(safely under it). Electronic history reaches back to ~2000; earlier windows
return empty. The ~300 monthly windows are fetched concurrently (the SOAP host
has no documented rate limit) so the whole corpus re-pulls in seconds, and we
re-fetch everything each run (revisions picked up for free) rather than keeping a
watermark.
"""

import concurrent.futures
from calendar import monthrange
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
# BCU's electronic daily series begin ~2000; 1999 is a safe floor (earlier
# windows return "No existe cotizacion" and yield no rows). The upper bound is
# the current month, discovered at run time — never hardcoded.
_FLOOR_YEAR = 1999
# Concurrency for the per-month window fetches. No documented rate limit on the
# SOAP host; modest fan-out keeps the full backfill to a few seconds.
_MAX_WORKERS = 8

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

    # respuestastatus.status: 1 = ok, 0 = no data / invalid window. An "excede"
    # message means our chunking exceeded the per-call span cap and would
    # silently drop data — that is our bug, so fail loudly.
    status = None
    mensaje = ""
    for el in root.iter():
        ln = _localname(el.tag)
        if ln == "status" and status is None:
            status = (el.text or "").strip()
        elif ln == "mensaje":
            mensaje = (el.text or "").strip()
    if mensaje and "excede" in mensaje.lower():
        raise AssertionError(
            f"window {desde}..{hasta} exceeded the BCU span cap ({mensaje}); shrink the chunk"
        )

    rows = []
    for dato in root.iter():
        if _localname(dato.tag) != "datoscotizaciones.dato":
            continue
        fields = {_localname(c.tag): (c.text.strip() if c.text else None) for c in dato}
        rows.append(fields)
    return rows


def _month_windows(floor_year: int, today: date) -> list[tuple[str, str]]:
    windows = []
    year, month = floor_year, 1
    while (year, month) <= (today.year, today.month):
        last = monthrange(year, month)[1]
        desde = f"{year}-{month:02d}-01"
        hasta = min(date(year, month, last), today).isoformat()
        windows.append((desde, hasta))
        month += 1
        if month > 12:
            month, year = 1, year + 1
    return windows


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
    windows = _month_windows(_FLOOR_YEAR, today)

    raw_rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=_MAX_WORKERS) as ex:
        # ex.map preserves window order and re-raises the first worker exception.
        for rows in ex.map(lambda w: _fetch_window(codes, w[0], w[1]), windows):
            raw_rows.extend(rows)

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
