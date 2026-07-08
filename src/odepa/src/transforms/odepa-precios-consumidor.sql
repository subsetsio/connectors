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
