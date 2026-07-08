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
