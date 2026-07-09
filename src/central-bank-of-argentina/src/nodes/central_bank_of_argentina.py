"""Central Bank of Argentina (BCRA) connector.

Mechanism: public REST API at https://api.bcra.gob.ar (no auth). Three subsets,
each fetched stateless/full every run (the whole corpus re-pulls in a few
minutes, so no watermark/cursor — revisions are picked up for free):

- monetary_series  : catalog of ~1581 monetary variables (one row per variable).
- monetary_values  : long-format daily/monthly observations for every variable
                     (paginated per-variable; ~millions of rows -> streamed).
- fx_quotations    : long-format official exchange-rate quotations per currency
                     (~44 currencies, daily since 1992-01-02).

API shape (probed):
- /estadisticas/v4.0/Monetarias            -> {results:[{idVariable, descripcion,
    categoria, tipoSerie, periodicidad, unidadExpresion, moneda, ...}], metadata}
    paginated by limit/offset (count 1581, max page 1000).
- /estadisticas/v4.0/Monetarias/{id}?desde=&hasta=  -> {results:[{idVariable,
    detalle:[{fecha, valor}]}], metadata}; detalle paginated by limit/offset.
- /estadisticascambiarias/v1.0/Maestros/Divisas -> {results:[{codigo, denominacion}]}.
- /estadisticascambiarias/v1.0/Cotizaciones/{code}?fechadesde=&fechahasta= ->
    {results:[{fecha, detalle:[{codigoMoneda, descripcion, tipoPase,
    tipoCotizacion}]}], metadata}; paginated by limit/offset. Min date 1992-01-02.
"""

from datetime import datetime, timezone

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

BASE = "https://api.bcra.gob.ar"
PAGE = 1000
MONETARY_MIN = "1900-01-01"   # API floors to each variable's first reported date
FX_MIN = "1992-01-02"          # API rejects fechadesde earlier than this


@transient_retry()
def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _today() -> str:
    return datetime.now(tz=timezone.utc).date().isoformat()


def _paginate(url: str, base_params: dict, extract):
    """Offset-paginate `url` until the reported resultset count is exhausted.

    `extract(results)` pulls the list of items out of one page's `results`
    payload (the shape differs per endpoint)."""
    offset = 0
    out = []
    while True:
        params = dict(base_params, limit=PAGE, offset=offset)
        data = _get_json(url, params)
        count = data.get("metadata", {}).get("resultset", {}).get("count", 0)
        items = extract(data.get("results"))
        out.extend(items)
        offset += PAGE
        if offset >= count or not items:
            break
    return out


# --------------------------------------------------------------------------- #
# Catalog enumeration
# --------------------------------------------------------------------------- #

def _fetch_catalog() -> list[dict]:
    """All monetary-variable definitions (~1581 rows)."""
    return _paginate(
        f"{BASE}/estadisticas/v4.0/Monetarias",
        {},
        lambda results: results or [],
    )


def _fetch_currencies() -> list[dict]:
    data = _get_json(f"{BASE}/estadisticascambiarias/v1.0/Maestros/Divisas", {})
    return data.get("results") or []


# --------------------------------------------------------------------------- #
# Download nodes
# --------------------------------------------------------------------------- #

_SERIES_SCHEMA = pa.schema([
    ("idVariable", pa.int64()),
    ("descripcion", pa.string()),
    ("categoria", pa.string()),
    ("tipoSerie", pa.string()),
    ("periodicidad", pa.string()),
    ("unidadExpresion", pa.string()),
    ("moneda", pa.string()),
    ("primerFechaInformada", pa.string()),
    ("ultFechaInformada", pa.string()),
    ("ultValorInformado", pa.float64()),
])

_SERIES_COLS = [f.name for f in _SERIES_SCHEMA]


def fetch_monetary_series(node_id: str) -> None:
    asset = node_id
    catalog = _fetch_catalog()
    rows = [{c: rec.get(c) for c in _SERIES_COLS} for rec in catalog]
    table = pa.Table.from_pylist(rows, schema=_SERIES_SCHEMA)
    save_raw_parquet(table, asset)


_CURRENCIES_SCHEMA = pa.schema([
    ("codigo", pa.string()),
    ("denominacion", pa.string()),
])

_CURRENCIES_COLS = [f.name for f in _CURRENCIES_SCHEMA]


def fetch_fx_currencies(node_id: str) -> None:
    """Currency master list (~44 rows: codigo, denominacion)."""
    asset = node_id
    currencies = _fetch_currencies()
    rows = [{c: rec.get(c) for c in _CURRENCIES_COLS} for rec in currencies]
    table = pa.Table.from_pylist(rows, schema=_CURRENCIES_SCHEMA)
    save_raw_parquet(table, asset)


_VALUES_SCHEMA = pa.schema([
    ("idVariable", pa.int64()),
    ("fecha", pa.string()),
    ("valor", pa.float64()),
])


def _fetch_series_points(var_id: int) -> list[dict]:
    url = f"{BASE}/estadisticas/v4.0/Monetarias/{var_id}"
    params = {"desde": MONETARY_MIN, "hasta": _today()}
    return _paginate(
        url,
        params,
        lambda results: (results[0].get("detalle") or []) if results else [],
    )


def fetch_monetary_values(node_id: str) -> None:
    asset = node_id
    catalog = _fetch_catalog()
    var_ids = [rec["idVariable"] for rec in catalog]
    with raw_parquet_writer(asset, _VALUES_SCHEMA) as writer:
        for var_id in var_ids:
            try:
                points = _fetch_series_points(var_id)
            except httpx.HTTPStatusError as e:
                if e.response.status_code in (400, 404):
                    print(f"  skip variable {var_id}: {e.response.status_code}")
                    continue
                raise
            if not points:
                continue
            rows = [
                {"idVariable": var_id, "fecha": p.get("fecha"), "valor": p.get("valor")}
                for p in points
            ]
            writer.write_table(pa.Table.from_pylist(rows, schema=_VALUES_SCHEMA))


_FX_SCHEMA = pa.schema([
    ("codigoMoneda", pa.string()),
    ("descripcion", pa.string()),
    ("fecha", pa.string()),
    ("tipoPase", pa.float64()),
    ("tipoCotizacion", pa.float64()),
])


def _fetch_currency_quotes(code: str) -> list[dict]:
    url = f"{BASE}/estadisticascambiarias/v1.0/Cotizaciones/{code}"
    params = {"fechadesde": FX_MIN, "fechahasta": _today()}

    def extract(results):
        out = []
        for day in results or []:
            fecha = day.get("fecha")
            for det in day.get("detalle") or []:
                out.append({
                    "codigoMoneda": det.get("codigoMoneda") or code,
                    "descripcion": det.get("descripcion"),
                    "fecha": fecha,
                    "tipoPase": det.get("tipoPase"),
                    "tipoCotizacion": det.get("tipoCotizacion"),
                })
        return out

    return _paginate(url, params, extract)


def fetch_fx_quotations(node_id: str) -> None:
    asset = node_id
    currencies = _fetch_currencies()
    with raw_parquet_writer(asset, _FX_SCHEMA) as writer:
        for cur in currencies:
            code = cur["codigo"]
            try:
                rows = _fetch_currency_quotes(code)
            except httpx.HTTPStatusError as e:
                if e.response.status_code in (400, 404):
                    print(f"  skip currency {code}: {e.response.status_code}")
                    continue
                raise
            if not rows:
                continue
            writer.write_table(pa.Table.from_pylist(rows, schema=_FX_SCHEMA))


DOWNLOAD_SPECS = [
    NodeSpec(id="central-bank-of-argentina-fx-currencies",
             fn=fetch_fx_currencies, kind="download"),
    NodeSpec(id="central-bank-of-argentina-monetary-series",
             fn=fetch_monetary_series, kind="download"),
    NodeSpec(id="central-bank-of-argentina-monetary-values",
             fn=fetch_monetary_values, kind="download"),
    NodeSpec(id="central-bank-of-argentina-fx-quotations",
             fn=fetch_fx_quotations, kind="download"),
]


# --------------------------------------------------------------------------- #
# Transforms — one published Delta table per subset
# --------------------------------------------------------------------------- #

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="central-bank-of-argentina-fx-currencies-transform",
        deps=["central-bank-of-argentina-fx-currencies"],
        sql='''
            SELECT DISTINCT
                codigo       AS currency_code,
                denominacion AS currency_name
            FROM "central-bank-of-argentina-fx-currencies"
            WHERE codigo IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="central-bank-of-argentina-monetary-series-transform",
        deps=["central-bank-of-argentina-monetary-series"],
        sql='''
            SELECT
                CAST(idVariable AS BIGINT)               AS variable_id,
                descripcion                              AS description,
                categoria                                AS category,
                tipoSerie                                AS series_type,
                periodicidad                             AS frequency,
                unidadExpresion                          AS unit,
                moneda                                   AS currency,
                TRY_CAST(primerFechaInformada AS DATE)   AS first_date,
                TRY_CAST(ultFechaInformada AS DATE)      AS last_date,
                CAST(ultValorInformado AS DOUBLE)        AS last_value
            FROM "central-bank-of-argentina-monetary-series"
            WHERE idVariable IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="central-bank-of-argentina-monetary-values-transform",
        deps=["central-bank-of-argentina-monetary-values"],
        sql='''
            SELECT DISTINCT
                CAST(idVariable AS BIGINT) AS variable_id,
                CAST(fecha AS DATE)        AS date,
                CAST(valor AS DOUBLE)      AS value
            FROM "central-bank-of-argentina-monetary-values"
            WHERE valor IS NOT NULL AND fecha IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="central-bank-of-argentina-fx-quotations-transform",
        deps=["central-bank-of-argentina-fx-quotations"],
        sql='''
            SELECT DISTINCT
                codigoMoneda             AS currency_code,
                descripcion              AS currency_name,
                CAST(fecha AS DATE)      AS date,
                CAST(tipoPase AS DOUBLE) AS rate_vs_usd,
                CAST(tipoCotizacion AS DOUBLE) AS rate_in_pesos
            FROM "central-bank-of-argentina-fx-quotations"
            WHERE fecha IS NOT NULL AND tipoCotizacion IS NOT NULL
        ''',
    ),
]
