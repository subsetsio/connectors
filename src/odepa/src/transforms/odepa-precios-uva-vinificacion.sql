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
