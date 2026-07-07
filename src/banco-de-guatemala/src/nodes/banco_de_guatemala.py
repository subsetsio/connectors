"""Banco de Guatemala (Banguat) connector.

The currently servable published subset is sourced from Banguat's verified
TipoCambio SOAP service:

  - exchange_rates  TipoCambioRango -> daily GTQ reference buy/sell exchange
                    rates, fetched year by year.

Fetch shape: stateless full re-pull (shape 1). TipoCambioRango takes an
explicit date window, so we request from a conservative early floor through
"today" and let the server return whatever history exists.

Transport note: the SOAP POSTs target https:// directly. The server 301-redirects
http -> https, and following that redirect downgrades the POST to a bodyless GET
(httpx redirect semantics) — which drops the SOAP envelope and makes BDEF return
500 and TipoCambio return its HTML help page. Posting straight to https keeps the
body intact. (Research flagged HTTPS cert issues seen from one probing host; the
cloud egress verifies the cert fine.)

The broader BDEF service is deliberately not used here: the endpoint returned
ASP.NET 500 from the GitHub runner and could not be verified locally.
"""

from datetime import datetime, timezone
import xml.etree.ElementTree as ET

import httpx

from subsets_utils import (
    NodeSpec,
    post,
    transient_retry,
    save_raw_ndjson,
)

NS = "http://www.banguat.gob.gt/variables/ws/"
TC_ENDPOINT = "https://www.banguat.gob.gt/variables/ws/TipoCambio.asmx"

# Conservative lower bounds — the API returns only the history it actually has;
# windows that reach before a series begins simply come back empty. These are
# floors for the request window, not fabricated coverage ranges.
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
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        # ASMX returns SOAP faults as HTTP 500 with an explanatory body; the bare
        # HTTPStatusError message drops it. Re-raise (still an HTTPStatusError, so
        # transient_retry keeps retrying 5xx) with the body appended so the run's
        # error tail reveals *why* the server faulted instead of an opaque 500.
        body = (resp.text or "")[:800].replace("\n", " ")
        raise httpx.HTTPStatusError(
            f"{e}; SOAPAction={NS}{op}; body: {body!r}",
            request=e.request,
            response=e.response,
        ) from e
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


def _now():
    return datetime.now(tz=timezone.utc)


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
    NodeSpec(id="banco-de-guatemala-exchange-rates", fn=fetch_exchange_rates, kind="download"),
]
