"""INE Spain (Instituto Nacional de Estadística) — Tempus3 JSON API connector.

Catalog connector. Each published subset is one INE statistical TABLE. The
full table — every series plus its complete time-series history — is returned
by a single GET to DATOS_TABLA/{table_id} (lang EN for English series names).
We flatten the nested {series -> Data[]} payload into long format and write one
parquet raw asset per table; a thin SQL transform publishes the Delta table.

Fetch shape: stateless full re-pull (shape 1). Each table is small enough to
re-fetch in full every run, and DATOS_TABLA returns the entire history with no
incremental filter needed — so no state, no watermark; we overwrite each run
and pick up revisions for free.
"""

import datetime

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet, transient_retry
from constants import ENTITY_IDS

SLUG = "national-statistics-institute"
PREFIX = f"{SLUG}-"
BASE = "https://servicios.ine.es/wstempus/js/EN"

# Explicit schema = the contract for every per-table parquet write.
SCHEMA = pa.schema([
    ("table_id", pa.int64()),
    ("series_cod", pa.string()),
    ("series_name", pa.string()),
    ("unit_id", pa.int64()),
    ("scale_id", pa.int64()),
    ("period_id", pa.int64()),
    ("data_type_id", pa.int64()),
    ("year", pa.int64()),
    ("date", pa.date32()),
    ("value", pa.float64()),
    ("secret", pa.bool_()),
])

# INE period reference timestamps are epoch-ms at Madrid local midnight (UTC-1/-2);
# shift +12h before taking the UTC date so the period lands on the intended day
# regardless of DST, without depending on a tz database being installed.
_DAY_SHIFT_MS = 12 * 3600 * 1000


@transient_retry()  # 6 attempts, exponential backoff over transient/429/5xx
def _fetch_table(table_id: str):
    resp = get(f"{BASE}/DATOS_TABLA/{table_id}", timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def _to_date(fecha_ms):
    if fecha_ms is None:
        return None
    return datetime.datetime.utcfromtimestamp(
        (fecha_ms + _DAY_SHIFT_MS) / 1000.0
    ).date()


def _to_int(v):
    return int(v) if isinstance(v, (int, float)) else None


def _to_float(v):
    return float(v) if isinstance(v, (int, float)) else None


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    table_id = node_id[len(PREFIX):]

    series_list = _fetch_table(table_id)
    if not isinstance(series_list, list):
        # An unexpected envelope (e.g. an error object) is a real surprise —
        # let it surface rather than silently writing an empty asset.
        raise TypeError(f"{asset}: DATOS_TABLA returned {type(series_list).__name__}, expected list")

    tid = int(table_id)
    rows = []
    for series in series_list:
        cod = series.get("COD")
        name = series.get("Nombre")
        unit = _to_int(series.get("FK_Unidad"))
        scale = _to_int(series.get("FK_Escala"))
        for dp in series.get("Data", []):
            rows.append({
                "table_id": tid,
                "series_cod": cod,
                "series_name": name,
                "unit_id": unit,
                "scale_id": scale,
                "period_id": _to_int(dp.get("FK_Periodo")),
                "data_type_id": _to_int(dp.get("FK_TipoDato")),
                "year": _to_int(dp.get("Anyo")),
                "date": _to_date(dp.get("Fecha")),
                "value": _to_float(dp.get("Valor")),
                "secret": bool(dp.get("Secreto")) if dp.get("Secreto") is not None else None,
            })

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST("date" AS DATE)      AS "date",
                table_id,
                series_cod,
                series_name,
                unit_id,
                CAST("year" AS INTEGER)   AS "year",
                CAST("value" AS DOUBLE)   AS "value"
            FROM "{s.id}"
            WHERE "value" IS NOT NULL AND "date" IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
