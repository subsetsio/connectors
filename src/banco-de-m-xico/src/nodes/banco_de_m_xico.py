"""Banco de México connector — SIE (Sistema de Información Económica) time series.

Access strategy (research-chosen mechanism `rest`):
  The SIE REST API exposes every Banxico economic time series, identified by stable
  ids like SF43718 / SP1. Data endpoints accept up to 100 comma-separated series
  ids per request and return full history as JSON in one shot:
    - GET /series/{ids}            -> per-series metadata (titulo, unidad, periodicidad)
    - GET /series/{ids}/datos      -> full history: [{fecha: "DD/MM/YYYY", dato: "..."}]
  Auth: a free, self-service 64-char token sent in the `Bmx-Token` header. The
  runtime supplies it via the BANXICO_TOKEN environment variable.

Entity scope:
  The rank step accepted a single subset, `values` — the long-format observation
  stream across SIE series. The SIE REST API has NO "list all series" endpoint
  (the ~50k-series catalogue lives only as a hierarchical web-portal tree), so a
  full-corpus crawl is not programmatically possible from the API alone. We
  therefore publish a curated set of the headline economic indicators Banxico is
  cited for — exchange rates, the policy (target) rate, TIIE/CETES money-market
  rates, monetary aggregates, international reserves, and prices (INPC/UDIS).
  Series metadata (title, unit, frequency) is folded in as columns rather than a
  separate `series` table (rank rejected that entity).

Refresh shape: stateless full re-pull. The curated corpus is small (a handful of
  series, full history each fetched in one batched request), so we re-fetch the
  whole thing every run and overwrite — late revisions to published figures are
  picked up for free, and no watermark can silently skip a revised observation.
"""
import os

import pyarrow as pa
from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://www.banxico.org.mx/SieAPIRest/service/v1/"

# Curated headline SIE series ids. Each is a stable, well-known Banxico indicator;
# titles/units come from the API metadata endpoint at fetch time, so this list is
# only the id set, grouped by sector for readability.
SERIES_IDS = [
    # Exchange rates (pesos per unit of foreign currency)
    "SF43718",   # USD/MXN, FIX
    "SF60653",   # USD/MXN, settlement (para solventar obligaciones)
    "SF46410",   # EUR/MXN
    "SF46406",   # JPY/MXN
    "SF46407",   # GBP/MXN
    "SF60632",   # CAD/MXN
    # Interest rates
    "SF61745",   # Tasa objetivo (policy/target rate)
    "SF43773",   # Tasa de fondeo bancario
    "SF60648",   # TIIE 28 days
    "SF60649",   # TIIE 91 days
    "SF60633",   # CETES 28 days, primary auction
    "SF60634",   # CETES 91 days, primary auction
    # Monetary aggregates
    "SF311408",  # M1
    "SF311418",  # M2
    # International reserves
    "SF43707",   # Reservas internacionales
    # Prices
    "SP1",       # INPC general (CPI)
    "SP68257",   # UDIS
]

# Raw is kept all-string: the API returns values as strings (with thousands
# separators and "N/E" sentinels) and dates as DD/MM/YYYY text. The transform
# owns parsing/typing so the cast failures surface there, not at write time.
SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("title",     pa.string()),
    ("unit",      pa.string()),
    ("frequency", pa.string()),
    ("fecha",     pa.string()),
    ("dato",      pa.string()),
])

# ---------------------------------------------------------------------------
# HTTP with honest retry + documented rate limit
# ---------------------------------------------------------------------------


# Documented historical-data limit is 200 requests / 5 min per token; use ~80%.
@sleep_and_retry
@limits(calls=160, period=300)
@transient_retry()
def _get_json(path: str, token: str) -> dict:
    resp = get(
        BASE + path,
        headers={"Bmx-Token": token, "Accept": "application/json"},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def _token() -> str:
    token = os.environ.get("BANXICO_TOKEN")
    if not token:
        raise RuntimeError(
            "BANXICO_TOKEN is not set; request a free token at "
            "https://www.banxico.org.mx/SieAPIRest/service/v1/token"
        )
    return token


def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    token = _token()
    rows = []

    # API allows up to 100 comma-separated ids per request.
    for batch in _chunks(SERIES_IDS, 100):
        ids = ",".join(batch)

        # Metadata: titulo / unidad / periodicidad per series.
        meta = {}
        for s in _get_json(f"series/{ids}", token).get("bmx", {}).get("series", []):
            meta[s["idSerie"]] = (
                s.get("titulo"),
                s.get("unidad"),
                s.get("periodicidad"),
            )

        # Full history.
        for s in _get_json(f"series/{ids}/datos", token).get("bmx", {}).get("series", []):
            sid = s["idSerie"]
            title, unit, freq = meta.get(sid, (s.get("titulo"), None, None))
            for obs in s.get("datos", []):
                rows.append({
                    "series_id": sid,
                    "title": title,
                    "unit": unit,
                    "frequency": freq,
                    "fecha": obs.get("fecha"),
                    "dato": obs.get("dato"),
                })

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="banco-de-m-xico-values", fn=fetch_values, kind="download"),
]


# ---------------------------------------------------------------------------
# Transform — one published Delta table. Parse DD/MM/YYYY dates, strip thousands
# separators and drop "N/E"/non-numeric observations, then cast value to double.
# A row is unique per (series_id, date).
# ---------------------------------------------------------------------------
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="banco-de-m-xico-values-transform",
        deps=["banco-de-m-xico-values"],
        sql='''
            SELECT
                series_id,
                title,
                unit,
                frequency,
                CAST(try_strptime(fecha, '%d/%m/%Y') AS DATE)   AS date,
                TRY_CAST(REPLACE(dato, ',', '') AS DOUBLE)      AS value
            FROM "banco-de-m-xico-values"
            WHERE fecha IS NOT NULL
              AND dato IS NOT NULL
              AND dato <> 'N/E'
              AND try_strptime(fecha, '%d/%m/%Y') IS NOT NULL
              AND TRY_CAST(REPLACE(dato, ',', '') AS DOUBLE) IS NOT NULL
        ''',
    ),
]
