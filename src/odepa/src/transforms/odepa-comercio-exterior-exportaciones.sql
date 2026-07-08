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
