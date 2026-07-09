"""INE (Spain) — Instituto Nacional de Estadística — INEbase JSON API connector.

One published Delta table per INE statistical *table* (the natural publication
unit on INEbase). Each table is fetched whole with a single
`DATOS_TABLA/{tableId}` request, which returns every series in the table with its
full historical Data array — no pagination. We flatten that to long format
(one row per series-observation) and publish it.

Fetch shape: stateless full re-pull. Each table is a single small request that
returns full history; revisions and late corrections are picked up for free by
always re-fetching. No watermark / cursor / state.

Resumability lives in `MAINTAIN_SPECS`: a table whose raw is already committed
and younger than the refresh window is skipped pre-spawn. That matters here
because a DAG invocation never resumes another one's node states — a run that
exhausts its time budget hands off to a continuation, and the continuation would
re-fetch everything it already has without a maintain skip. The raw manifest
spans runs, so `raw_asset_exists` is what makes the 5000-node backfill converge.

Per-entity robustness: a single table must never fail the whole DAG. DATOS_TABLA
answers with a JSON *dict* instead of the usual list in three cases:

  - "Peticion en proceso ..."               — INE is materializing the response
                                              server-side. TRANSIENT: re-ask.
  - "No puede mostrarse por restricciones
     de volumen"                            — the table has too many series for
                                              the endpoint to serve. Permanent,
                                              and unfixable from here: nult=,
                                              date=, tv= and SERIES_TABLA are all
                                              refused the same way.
  - "No existen series para la tabla"       — the table is declared but empty.

The permanent two are disqualified at the accept stage, so reaching one here is
an upstream change, not routine: it is logged and skipped (raw left absent)
rather than raised, so it can't abort a 5000-node run.
"""

import time
from datetime import date, datetime, timezone

import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_IDS

BASE = "https://servicios.ine.es/wstempus/js/ES"

# A fetched table is considered fresh (skipped) for this many days. INE publishes
# a per-operation release calendar (https://www.ine.es/dyngs/INEbase/es/calendario.htm)
# rather than one corpus-wide cadence, and the most frequent tables are monthly —
# so this is an inferred window, sized under a month to catch monthly releases
# while letting continuation legs of one backfill skip what earlier legs
# committed.
MAINTAIN_MAX_AGE_DAYS = 20

# Dict-payload statuses, ASCII-folded (INE's own accents are inconsistent).
_IN_PROCESS = "Peticion en proceso"
_PERMANENT = ("restricciones de volumen", "No existen series")

# Long-format raw schema. Declared once, reused for every table's write — the
# explicit schema is the contract that makes parquet safe across all 5000+ nodes.
SCHEMA = pa.schema([
    ("table_id", pa.string()),
    ("serie_cod", pa.string()),
    ("serie_nombre", pa.string()),
    ("fk_unidad", pa.int64()),
    ("fk_escala", pa.int64()),
    ("fecha_ms", pa.int64()),
    ("anyo", pa.int64()),
    ("fk_periodo", pa.int64()),
    ("fk_tipodato", pa.int64()),
    ("valor", pa.float64()),
    ("secreto", pa.bool_()),
])


def _fold(text: str) -> str:
    """Drop non-ASCII so status matching survives INE's inconsistent accents."""
    return (text or "").encode("ascii", "ignore").decode()


@transient_retry()  # 6 attempts, exponential backoff over transient errors + 429 + 5xx
def _fetch_once(table_id: str):
    """One network fetch of a table's DATOS_TABLA payload (parsed JSON).

    The retry decorator only covers network-layer failures (connect/read
    timeouts, 429, 5xx). INE intermittently answers a rapid sequence of requests
    with an empty 200 body; that is transient too, so raise into the same retry.
    """
    resp = get(f"{BASE}/DATOS_TABLA/{table_id}", timeout=(10.0, 300.0))
    resp.raise_for_status()
    if not resp.content or not resp.content.strip():
        raise ValueError(f"empty body for table {table_id}")
    return resp.json()


class _PermanentlyUnservable(Exception):
    """DATOS_TABLA refuses this table for good (volume restriction / no series)."""


def _fetch_table(table_id: str, *, in_process_attempts: int = 5) -> list:
    """Fetch one INE table whole, returning its list of series dicts.

    A dict payload is either INE still computing the answer (retry, it resolves
    within a minute or two) or a permanent refusal (raise `_PermanentlyUnservable`
    for the caller to log and skip).
    """
    for attempt in range(in_process_attempts):
        data = _fetch_once(table_id)
        if isinstance(data, list):
            return data
        status = data.get("status", "") if isinstance(data, dict) else repr(data)
        folded = _fold(status)
        if any(p in folded for p in _PERMANENT):
            raise _PermanentlyUnservable(status)
        if not folded.startswith(_IN_PROCESS):
            raise ValueError(f"unexpected payload for table {table_id}: {status!r}")
        time.sleep(15 * (attempt + 1))
    raise ValueError(f"table {table_id} still 'in process' after {in_process_attempts} attempts")


def _to_rows(table_id: str, series: list) -> list[dict]:
    rows = []
    for s in series:
        cod = s.get("COD")
        nombre = s.get("Nombre")
        fk_unidad = s.get("FK_Unidad")
        fk_escala = s.get("FK_Escala")
        for pt in s.get("Data") or []:
            valor = pt.get("Valor")
            rows.append({
                "table_id": table_id,
                "serie_cod": cod,
                "serie_nombre": nombre,
                "fk_unidad": fk_unidad,
                "fk_escala": fk_escala,
                "fecha_ms": pt.get("Fecha"),
                "anyo": pt.get("Anyo"),
                "fk_periodo": pt.get("FK_Periodo"),
                "fk_tipodato": pt.get("FK_TipoDato"),
                "valor": float(valor) if valor is not None else None,
                "secreto": pt.get("Secreto"),
            })
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    table_id = node_id[len("ine-"):]  # recover the entity from the id

    try:
        series = _fetch_table(table_id)
    except _PermanentlyUnservable as exc:
        # Disqualified at accept, so this is upstream drift. Leave raw absent
        # rather than abort the run; the missing table surfaces downstream.
        print(f"[ine] {table_id}: skipped, DATOS_TABLA refuses it: {exc}")
        return

    rows = _to_rows(table_id, series)
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)
    print(f"[ine] {table_id}: {len(rows)} rows from {len(series)} series")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ine-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


def _is_fresh(asset_id: str) -> bool:
    """Skip policy: raw already committed and younger than the refresh window."""
    return raw_asset_exists(asset_id, "parquet", max_age_days=MAINTAIN_MAX_AGE_DAYS)


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=s.id,
        description=(
            f"Full re-pull when raw is older than {MAINTAIN_MAX_AGE_DAYS}d "
            "(inferred window — INE publishes a per-operation release calendar, "
            "https://www.ine.es/dyngs/INEbase/es/calendario.htm, not one corpus "
            "cadence; the shortest is monthly). Also makes the backfill resumable "
            "across continuation legs."
        ),
        check=_is_fresh,
    )
    for s in DOWNLOAD_SPECS
]
