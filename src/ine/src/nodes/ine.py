"""INE (Spain) — Instituto Nacional de Estadística — INEbase JSON API connector.

One published Delta table per INE statistical *table* (the natural publication
unit on INEbase). Each table is fetched whole with a single
`DATOS_TABLA/{tableId}` request, which returns every series in the table with its
full historical Data array — no pagination. We flatten that to long format
(one row per series-observation) and publish it.

Fetch shape: stateless full re-pull. Each table is a single small request that
returns full history; revisions and late corrections are picked up for free by
always re-fetching. No watermark / cursor / state.
"""

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)
from constants import ENTITY_IDS

BASE = "https://servicios.ine.es/wstempus/js/ES"

# Long-format raw schema. Declared once, reused for every table's write — the
# explicit schema is the contract that makes parquet safe across all 4728 nodes.
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


@transient_retry()  # 6 attempts, exponential backoff over transient errors + 429 + 5xx
def _fetch_table(table_id: str) -> list:
    """Fetch one INE table whole. Returns the list of series dicts.

    Treats an empty body as transient (INE intermittently returns empty 200s on
    rapid sequential requests) so the retry decorator backs off and retries.
    """
    resp = get(f"{BASE}/DATOS_TABLA/{table_id}", timeout=(10.0, 180.0))
    resp.raise_for_status()
    if not resp.content or not resp.content.strip():
        raise ValueError(f"empty body for table {table_id}")
    data = resp.json()
    if not isinstance(data, list):
        # API returns a list of series; anything else is an unexpected payload
        raise ValueError(f"unexpected payload type {type(data)} for table {table_id}")
    return data


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    table_id = node_id[len("ine-"):]  # recover the entity from the id

    series = _fetch_table(table_id)

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

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ine-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per subset: parse fecha (epoch ms) to a real DATE,
# type valor, keep the dimensional context (series + unit/scale codes). Rows
# without a date are dropped; values may legitimately be null (suppressed cells).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                make_timestamp(fecha_ms * 1000)::DATE AS date,
                anyo                                   AS year,
                fk_periodo                             AS period_code,
                serie_cod                              AS series_code,
                serie_nombre                           AS series_name,
                fk_unidad                              AS unit_code,
                fk_escala                              AS scale_code,
                fk_tipodato                            AS data_type_code,
                CAST(valor AS DOUBLE)                  AS value,
                secreto                                AS is_confidential
            FROM "{s.id}"
            WHERE fecha_ms IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
