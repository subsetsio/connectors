"""ODEPA (Oficina de Estudios y Politicas Agrarias, Chile) connector.

Source: https://datos.odepa.gob.cl — a standard CKAN 3 portal. Each of the 6
packages partitions its data into one CSV resource per year. We discover the
resource list per package via the CKAN `package_show` action API, then download
every yearly CSV at its stable per-resource download URL (one GET each, full
content, no pagination) and concatenate them into one raw ndjson asset per
subset.

Fetch shape: stateless full re-pull. The whole corpus is small (agricultural
price/trade tables, tens of MB per subset) and CKAN exposes no reliable
modified-since filter, so we re-fetch every yearly CSV each run and overwrite.
Only the current/recent year files actually change upstream; re-pulling the
historical years is cheap and picks up any revisions for free.

Raw format: ndjson (streamed, gzip). CSV headers are stable within each package
across all years (verified 1998..2026 for trade, 2008..2026 for consumer prices,
1999..2025 for the fruit cadastre), but values are kept as strings — several
numeric columns use a decimal comma ("11890,000000"), which the transform SQL
normalises. ndjson also tolerates any future per-year column drift for free.

`comercio-exterior` is published as two subsets: exports (Region origen / Pais
destino / USD FOB) and imports (Pais origen / USD CIF) carry different column
lists, so each is its own table.
"""

import csv
import io
import json

from constants import ENTITY_SPECS
from subsets_utils import NodeSpec, SqlNodeSpec, get, raw_writer, transient_retry

CKAN = "https://datos.odepa.gob.cl/api/3/action"


@transient_retry()
def _get_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        raise AssertionError(f"CKAN reported failure for {url}: {payload.get('error')}")
    return payload["result"]


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _csv_resources(package: str, flow: str | None) -> list[dict]:
    pkg = _get_json(f"{CKAN}/package_show?id={package}")
    resources = [r for r in pkg.get("resources", []) if (r.get("format") or "").upper() == "CSV"]
    if flow:
        resources = [
            r for r in resources
            if flow in (r.get("name") or "").lower() or flow in (r.get("url") or "").lower()
        ]
    return resources


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity_id = node_id[len("odepa-"):]
    spec = ENTITY_SPECS[entity_id]

    resources = _csv_resources(spec["package"], spec["flow"])
    if not resources:
        raise AssertionError(f"no CSV resources discovered for {entity_id} (package={spec['package']})")

    rows_written = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for res in resources:
            url = res["url"]
            text = _get_bytes(url).decode("utf-8-sig", errors="replace")
            reader = csv.DictReader(io.StringIO(text))
            for row in reader:
                # Drop the ragged-row overflow key csv.DictReader emits as None.
                row.pop(None, None)
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                rows_written += 1

    if rows_written == 0:
        raise AssertionError(f"fetched 0 rows for {entity_id} across {len(resources)} resources")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"odepa-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_SPECS
]


# --- Transforms: one published Delta table per subset. Thin parse-and-type over
# the raw ndjson. Numeric columns with a decimal comma are normalised with
# REPLACE(x, ',', '.'); TRY_CAST keeps a single malformed historical row from
# failing the whole node. Quoted identifiers because the source headers carry
# spaces and accents. ---

_SQL = {
    "odepa-precios-consumidor": '''
        SELECT
            TRY_CAST("Anio" AS INTEGER)               AS anio,
            TRY_CAST("Mes" AS INTEGER)                AS mes,
            TRY_CAST("Semana" AS INTEGER)             AS semana,
            TRY_CAST("Fecha inicio" AS DATE)          AS fecha_inicio,
            TRY_CAST("Fecha termino" AS DATE)         AS fecha_termino,
            TRY_CAST("ID region" AS INTEGER)          AS id_region,
            "Region"                                   AS region,
            "Sector"                                   AS sector,
            "Tipo de punto monitoreo"                  AS tipo_punto_monitoreo,
            "Grupo"                                     AS grupo,
            "Producto"                                 AS producto,
            "Unidad"                                   AS unidad,
            TRY_CAST(REPLACE("Precio minimo", ',', '.') AS DOUBLE)   AS precio_minimo,
            TRY_CAST(REPLACE("Precio maximo", ',', '.') AS DOUBLE)   AS precio_maximo,
            TRY_CAST(REPLACE("Precio promedio", ',', '.') AS DOUBLE) AS precio_promedio
        FROM "odepa-precios-consumidor"
        WHERE "Producto" IS NOT NULL AND "Anio" IS NOT NULL
    ''',
    "odepa-comercio-exterior-exportaciones": '''
        SELECT
            TRY_CAST("Anio" AS INTEGER)      AS anio,
            TRY_CAST("Mes" AS INTEGER)       AS mes,
            "Codigo producto"                 AS codigo_producto,
            "Producto"                        AS producto,
            TRY_CAST("ID region" AS INTEGER) AS id_region,
            "Region origen"                   AS region_origen,
            "Pais destino"                    AS pais_destino,
            "Unidad"                          AS unidad,
            TRY_CAST(REPLACE("Volumen", ',', '.') AS DOUBLE) AS volumen,
            TRY_CAST(REPLACE("USD FOB", ',', '.') AS DOUBLE) AS usd_fob
        FROM "odepa-comercio-exterior-exportaciones"
        WHERE "Producto" IS NOT NULL AND "Anio" IS NOT NULL
    ''',
    "odepa-comercio-exterior-importaciones": '''
        SELECT
            TRY_CAST("Anio" AS INTEGER) AS anio,
            TRY_CAST("Mes" AS INTEGER)  AS mes,
            "Codigo producto"            AS codigo_producto,
            "Producto"                   AS producto,
            "Pais origen"                AS pais_origen,
            "Unidad"                     AS unidad,
            TRY_CAST(REPLACE("Volumen", ',', '.') AS DOUBLE) AS volumen,
            TRY_CAST(REPLACE("USD CIF", ',', '.') AS DOUBLE) AS usd_cif
        FROM "odepa-comercio-exterior-importaciones"
        WHERE "Producto" IS NOT NULL AND "Anio" IS NOT NULL
    ''',
    "odepa-precios-mayoristas-de-flores-y-follajes": '''
        SELECT
            TRY_CAST("Fecha" AS DATE)        AS fecha,
            TRY_CAST("ID region" AS INTEGER) AS id_region,
            "Region"                          AS region,
            "Mercado"                         AS mercado,
            "Subsector"                       AS subsector,
            "Producto"                        AS producto,
            "Variedad / Tipo"                 AS variedad_tipo,
            "Calidad"                         AS calidad,
            "Unidad de comercializacion"      AS unidad_comercializacion,
            "Origen"                          AS origen,
            TRY_CAST(REPLACE("Precio minimo", ',', '.') AS DOUBLE)   AS precio_minimo,
            TRY_CAST(REPLACE("Precio maximo", ',', '.') AS DOUBLE)   AS precio_maximo,
            TRY_CAST(REPLACE("Precio promedio", ',', '.') AS DOUBLE) AS precio_promedio
        FROM "odepa-precios-mayoristas-de-flores-y-follajes"
        WHERE "Producto" IS NOT NULL AND "Fecha" IS NOT NULL
    ''',
    "odepa-precios-mayoristas-de-frutas-y-hortalizas": '''
        SELECT
            TRY_CAST("Fecha" AS DATE)        AS fecha,
            TRY_CAST("ID region" AS INTEGER) AS id_region,
            "Region"                          AS region,
            "Mercado"                         AS mercado,
            "Subsector"                       AS subsector,
            "Producto"                        AS producto,
            "Variedad / Tipo"                 AS variedad_tipo,
            "Calidad"                         AS calidad,
            "Unidad de comercializacion"      AS unidad_comercializacion,
            "Origen"                          AS origen,
            TRY_CAST(REPLACE("Volumen", ',', '.') AS DOUBLE)         AS volumen,
            TRY_CAST(REPLACE("Precio minimo", ',', '.') AS DOUBLE)   AS precio_minimo,
            TRY_CAST(REPLACE("Precio maximo", ',', '.') AS DOUBLE)   AS precio_maximo,
            TRY_CAST(REPLACE("Precio promedio", ',', '.') AS DOUBLE) AS precio_promedio
        FROM "odepa-precios-mayoristas-de-frutas-y-hortalizas"
        WHERE "Producto" IS NOT NULL AND "Fecha" IS NOT NULL
    ''',
    "odepa-precios-uva-vinificacion": '''
        SELECT
            TRY_CAST("Anio" AS INTEGER)             AS anio,
            TRY_CAST("Mes" AS INTEGER)              AS mes,
            TRY_CAST("Fecha precio vigente" AS DATE) AS fecha_precio_vigente,
            TRY_CAST("ID region" AS INTEGER)        AS id_region,
            "Region"                                 AS region,
            "Comuna"                                 AS comuna,
            "Poder comprador"                        AS poder_comprador,
            "Sucursal"                               AS sucursal,
            "Variedad"                               AS variedad,
            TRY_CAST(REPLACE("Precio", ',', '.') AS DOUBLE)      AS precio,
            TRY_CAST(REPLACE("Grado brix", ',', '.') AS DOUBLE)  AS grado_brix,
            TRY_CAST("Fecha proximo precio" AS DATE) AS fecha_proximo_precio,
            TRY_CAST(REPLACE("Proximo precio", ',', '.') AS DOUBLE) AS proximo_precio,
            "Observaciones"                          AS observaciones
        FROM "odepa-precios-uva-vinificacion"
        WHERE "Variedad" IS NOT NULL AND "Anio" IS NOT NULL
    ''',
    "odepa-catastro-fruticola": '''
        SELECT
            TRY_CAST("Anio" AS INTEGER)      AS anio,
            TRY_CAST("ID region" AS INTEGER) AS id_region,
            "Region"                          AS region,
            "Provincia"                       AS provincia,
            "Comuna"                          AS comuna,
            "Número explotación"              AS numero_explotacion,
            "Número bloque"                   AS numero_bloque,
            "Tipo productor"                  AS tipo_productor,
            "Especie"                         AS especie,
            "Variedad"                        AS variedad,
            TRY_CAST("Anio plantacion" AS INTEGER)   AS anio_plantacion,
            "Metodo de riego"                 AS metodo_de_riego,
            TRY_CAST(REPLACE("Numero de arboles", ',', '.') AS DOUBLE) AS numero_de_arboles,
            TRY_CAST(REPLACE("Superficie (ha)", ',', '.') AS DOUBLE)   AS superficie_ha
        FROM "odepa-catastro-fruticola"
        WHERE "Especie" IS NOT NULL AND "Anio" IS NOT NULL
    ''',
}


TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_SQL[s.id])
    for s in DOWNLOAD_SPECS
]
