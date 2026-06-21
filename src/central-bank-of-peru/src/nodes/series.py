"""``central-bank-of-peru-series`` — the full BCRPData series catalog.

One row per series (code, category, group, name, unit, frequency, span),
sourced from the single semicolon-delimited, ISO-8859-1 metadata file at
``/estadisticas/series/metadata``.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import (
    _C_CODE, _C_CAT, _C_GRP, _C_NAME, _C_DESC,
    _C_GEO, _C_SOURCE, _C_FREQ,
    _C_PUBGRP, _C_AREA, _C_UPDATED, _C_START, _C_END,
    _cell,
    _fetch_catalog_rows,
)

_CATALOG_SCHEMA = pa.schema([
    ("codigo_serie", pa.string()),
    ("categoria", pa.string()),
    ("grupo", pa.string()),
    ("nombre", pa.string()),
    ("descripcion", pa.string()),
    ("geografia", pa.string()),
    ("fuente", pa.string()),
    ("frecuencia", pa.string()),
    ("grupo_publicacion", pa.string()),
    ("area_publica", pa.string()),
    ("fecha_actualizacion", pa.string()),
    ("fecha_inicio", pa.string()),
    ("fecha_fin", pa.string()),
])


def fetch_series(node_id: str) -> None:
    """Download and store the full BCRPData series catalog (one row per series)."""
    asset = node_id
    rows = _fetch_catalog_rows()
    cols = {name: [] for name in _CATALOG_SCHEMA.names}
    for r in rows:
        cols["codigo_serie"].append(_cell(r, _C_CODE))
        cols["categoria"].append(_cell(r, _C_CAT))
        cols["grupo"].append(_cell(r, _C_GRP))
        cols["nombre"].append(_cell(r, _C_NAME))
        cols["descripcion"].append(_cell(r, _C_DESC))
        cols["geografia"].append(_cell(r, _C_GEO))
        cols["fuente"].append(_cell(r, _C_SOURCE))
        cols["frecuencia"].append(_cell(r, _C_FREQ))
        cols["grupo_publicacion"].append(_cell(r, _C_PUBGRP))
        cols["area_publica"].append(_cell(r, _C_AREA))
        cols["fecha_actualizacion"].append(_cell(r, _C_UPDATED))
        cols["fecha_inicio"].append(_cell(r, _C_START))
        cols["fecha_fin"].append(_cell(r, _C_END))
    table = pa.table(cols, schema=_CATALOG_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="central-bank-of-peru-series", fn=fetch_series, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="central-bank-of-peru-series-transform",
        deps=["central-bank-of-peru-series"],
        sql='''
            SELECT
                codigo_serie,
                NULLIF(categoria, '')          AS categoria,
                NULLIF(grupo, '')              AS grupo,
                NULLIF(nombre, '')             AS nombre,
                NULLIF(descripcion, '')        AS descripcion,
                NULLIF(geografia, '')          AS geografia,
                NULLIF(fuente, '')             AS fuente,
                NULLIF(frecuencia, '')         AS frecuencia,
                NULLIF(grupo_publicacion, '')  AS grupo_publicacion,
                NULLIF(area_publica, '')       AS area_publica,
                NULLIF(fecha_actualizacion,'') AS fecha_actualizacion,
                NULLIF(fecha_inicio, '')       AS fecha_inicio,
                NULLIF(fecha_fin, '')          AS fecha_fin
            FROM "central-bank-of-peru-series"
            WHERE codigo_serie IS NOT NULL AND codigo_serie <> ''
        ''',
    ),
]
