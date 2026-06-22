"""Banco de Guatemala (Banguat) connector.

Three published subsets, all sourced from Banguat's SOAP web services
(verified contract from the BDEF.asmx / TipoCambio.asmx WSDLs):

  - variables       BDEF VariablesDisponibles -> catalog of every economic /
                    financial variable (ID, Nombre). Reference table.
  - values          BDEF Info{Mensual,Anual,Diario,Semanal} -> long-format
                    (variable, date, value) history. The primary subset.
  - exchange_rates  TipoCambio TipoCambioRango -> daily GTQ reference buy/sell
                    exchange rates (per currency id), year by year.

Fetch shape: stateless full re-pull (shape 1). The corpus is modest (a few
hundred variables of monthly/annual/daily points, plus daily FX) and the
SOAP API exposes no incremental/`since` filter, so every run re-pulls the full
history and overwrites. The Info* operations and TipoCambioRango take an
explicit date window, so we request from a conservative early floor through
"today" and let the server return whatever history exists.

Transport note: the SOAP POSTs target https:// directly. The server 301-redirects
http -> https, and following that redirect downgrades the POST to a bodyless GET
(httpx redirect semantics) — which drops the SOAP envelope and makes BDEF return
500 and TipoCambio return its HTML help page. Posting straight to https keeps the
body intact. (Research flagged HTTPS cert issues seen from one probing host; the
cloud egress verifies the cert fine.)

BDEF exposes no per-variable frequency in its catalog, so `values` cascades
the four frequency operations per variable (monthly -> annual -> daily ->
weekly) and keeps the first that returns data, tagging each row with its
frequency.
"""

from datetime import datetime, timezone
import xml.etree.ElementTree as ET

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    post,
    transient_retry,
    save_raw_parquet,
    save_raw_ndjson,
)

NS = "http://www.banguat.gob.gt/variables/ws/"
BDEF_ENDPOINT = "https://www.banguat.gob.gt/variables/ws/BDEF.asmx"  # https direct: avoid POST->GET on redirect
TC_ENDPOINT = "https://www.banguat.gob.gt/variables/ws/TipoCambio.asmx"

# Conservative lower bounds — the API returns only the history it actually has;
# windows that reach before a series begins simply come back empty. These are
# floors for the request window, not fabricated coverage ranges.
EARLIEST_YEAR_SERIES = 1950
EARLIEST_YEAR_FX = 1990


# --- SOAP plumbing -------------------------------------------------------

@transient_retry()  # 6 attempts, exp backoff; retries 429/5xx/network, then reraises
def _soap_call(endpoint: str, op: str, params: list[tuple[str, object]]) -> ET.Element:
    """POST a SOAP 1.1 request and return the parsed root element.

    `params` is an ordered list of (name, value) — order matters for ASMX
    sequence types. Returns the XML root; callers locate result elements by
    local name (namespace-agnostic).
    """
    inner = "".join(f"<{k}>{v}</{k}>" for k, v in params)
    envelope = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
        f'<soap:Body><{op} xmlns="{NS}">{inner}</{op}></soap:Body>'
        "</soap:Envelope>"
    )
    resp = post(
        endpoint,
        data=envelope.encode("utf-8"),
        headers={
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": f'"{NS}{op}"',
        },
        timeout=(15.0, 240.0),
    )
    resp.raise_for_status()
    try:
        return ET.fromstring(resp.content)
    except ET.ParseError as e:
        head = resp.text[:300].replace("\n", " ")
        raise AssertionError(
            f"{op}: response was not well-formed XML ({e}); "
            f"content-type={resp.headers.get('content-type')!r}; body starts: {head!r}"
        ) from e


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _iter_named(root: ET.Element, name: str):
    for el in root.iter():
        if _local(el.tag) == name:
            yield el


def _child_text(el: ET.Element, name: str):
    for c in el:
        if _local(c.tag) == name:
            return (c.text or "").strip()
    return None


def _to_float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _to_int(v):
    if v is None or v == "":
        return None
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def _list_variables() -> list[tuple[str, str]]:
    """VariablesDisponibles -> [(ID, Nombre), ...]."""
    root = _soap_call(BDEF_ENDPOINT, "VariablesDisponibles", [])
    out = []
    for var in _iter_named(root, "Variable"):
        vid = _child_text(var, "ID")
        nombre = _child_text(var, "Nombre")
        if vid:
            out.append((vid, nombre or vid))
    if not out:
        raise AssertionError("VariablesDisponibles returned no variables")
    return out


# --- variables -----------------------------------------------------------

def fetch_variables(node_id: str) -> None:
    asset = node_id
    rows = [{"variable_id": vid, "nombre": nombre} for vid, nombre in _list_variables()]
    table = pa.Table.from_pylist(
        rows,
        schema=pa.schema([("variable_id", pa.string()), ("nombre", pa.string())]),
    )
    save_raw_parquet(table, asset)


# --- values --------------------------------------------------------------

def _now():
    return datetime.now(tz=timezone.utc)


def _frequency_plan(variable_id: str):
    """Ordered (frequency, op, params, datum_element) attempts for one variable."""
    now = _now()
    y, m = now.year, now.month
    today = now.strftime("%d/%m/%Y")
    return [
        ("monthly", "InfoMensual",
         [("mes_inicial", 1), ("anio_inicial", EARLIEST_YEAR_SERIES),
          ("mes_final", m), ("anio_final", y), ("variable", variable_id)],
         "dMensual"),
        ("annual", "InfoAnual",
         [("anio_inicial", EARLIEST_YEAR_SERIES), ("anio_final", y),
          ("variable", variable_id)],
         "dAnual"),
        ("daily", "InfoDiario",
         [("fecha_inicial_ddmmaaaa", f"01/01/{EARLIEST_YEAR_SERIES}"),
          ("fecha_final_ddmmaaaa", today), ("variable", variable_id)],
         "dDiario"),
        ("weekly", "InfoSemanal",
         [("semana_inicial", 1), ("anio_inicial", EARLIEST_YEAR_SERIES),
          ("semana_final", 53), ("anio_final", y), ("variable", variable_id)],
         "dSemanal"),
    ]


def _parse_datum(freq: str, el: ET.Element) -> dict:
    return {
        "frequency": freq,
        "anio": _to_int(_child_text(el, "Anio")),
        "mes": _to_int(_child_text(el, "Mes")),
        "semana": _to_int(_child_text(el, "Semana")),
        "fecha": _child_text(el, "Fecha"),
        "monto": _to_float(_child_text(el, "Monto")),
    }


def fetch_values(node_id: str) -> None:
    asset = node_id
    variables = _list_variables()
    rows = []
    for vid, nombre in variables:
        for freq, op, params, datum in _frequency_plan(vid):
            root = _soap_call(BDEF_ENDPOINT, op, params)
            data = list(_iter_named(root, datum))
            if not data:
                continue
            for el in data:
                rec = _parse_datum(freq, el)
                rec["variable_id"] = vid
                rec["variable_name"] = nombre
                rows.append(rec)
            break  # first frequency with data wins
    if not rows:
        raise AssertionError("values: no observations returned for any variable")
    save_raw_ndjson(rows, asset)


# --- exchange_rates ------------------------------------------------------

def fetch_exchange_rates(node_id: str) -> None:
    asset = node_id
    now = _now()
    rows = []
    for year in range(EARLIEST_YEAR_FX, now.year + 1):
        fin = "31/12" if year < now.year else now.strftime("%d/%m")
        root = _soap_call(
            TC_ENDPOINT,
            "TipoCambioRango",
            [("fechainit", f"01/01/{year}"), ("fechafin", f"{fin}/{year}")],
        )
        for var in _iter_named(root, "Var"):
            rows.append({
                "moneda": _to_int(_child_text(var, "moneda")),
                "fecha": _child_text(var, "fecha"),
                "venta": _to_float(_child_text(var, "venta")),
                "compra": _to_float(_child_text(var, "compra")),
            })
    if not rows:
        raise AssertionError("exchange_rates: TipoCambioRango returned no rows for any year")
    save_raw_ndjson(rows, asset)


# --- specs ---------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="banco-de-guatemala-variables", fn=fetch_variables, kind="download"),
    NodeSpec(id="banco-de-guatemala-values", fn=fetch_values, kind="download"),
    NodeSpec(id="banco-de-guatemala-exchange-rates", fn=fetch_exchange_rates, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="banco-de-guatemala-variables-transform",
        deps=["banco-de-guatemala-variables"],
        sql='''
            SELECT
                CAST(variable_id AS VARCHAR) AS variable_id,
                CAST(nombre AS VARCHAR)      AS name
            FROM "banco-de-guatemala-variables"
            WHERE variable_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="banco-de-guatemala-values-transform",
        deps=["banco-de-guatemala-values"],
        sql='''
            SELECT * FROM (
                SELECT
                    CAST(variable_id AS VARCHAR)   AS variable_id,
                    CAST(variable_name AS VARCHAR) AS variable_name,
                    CAST(frequency AS VARCHAR)     AS frequency,
                    CASE frequency
                        WHEN 'daily'   THEN CAST(fecha AS DATE)
                        WHEN 'monthly' THEN make_date(CAST(anio AS INTEGER), CAST(mes AS INTEGER), 1)
                        WHEN 'annual'  THEN make_date(CAST(anio AS INTEGER), 1, 1)
                        WHEN 'weekly'  THEN make_date(CAST(anio AS INTEGER), 1, 1)
                                             + ((CAST(semana AS INTEGER) - 1) * 7) * INTERVAL 1 DAY
                    END AS date,
                    CAST(monto AS DOUBLE)          AS value
                FROM "banco-de-guatemala-values"
                WHERE monto IS NOT NULL
            )
            WHERE date IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="banco-de-guatemala-exchange-rates-transform",
        deps=["banco-de-guatemala-exchange-rates"],
        sql='''
            SELECT
                strptime(CAST(fecha AS VARCHAR), '%d/%m/%Y')::DATE AS date,
                CAST(moneda AS INTEGER) AS currency_id,
                CAST(compra AS DOUBLE)  AS buy,
                CAST(venta AS DOUBLE)   AS sell
            FROM "banco-de-guatemala-exchange-rates"
            WHERE fecha IS NOT NULL
              AND (compra IS NOT NULL OR venta IS NOT NULL)
        ''',
    ),
]
