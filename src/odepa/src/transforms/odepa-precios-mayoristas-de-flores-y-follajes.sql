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
