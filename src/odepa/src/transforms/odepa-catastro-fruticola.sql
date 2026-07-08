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
