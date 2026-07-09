-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns), then curated: Spanish source columns
-- renamed to snake_case English; casts unchanged from the compile.
-- caution: One row per series (the series dimension/catalog), not an observation table — join to central-bank-of-peru-values on series_code to attach labels, unit and frequency to the observations.
SELECT
    "codigo_serie"                                  AS series_code,
    "categoria"                                     AS category,
    "grupo"                                         AS series_group,
    "nombre"                                        AS name,
    "descripcion"                                   AS description,
    "geografia"                                     AS geography,
    "fuente"                                        AS source,
    "frecuencia"                                    AS frequency,
    "grupo_publicacion"                             AS publication_group,
    "area_publica"                                  AS public_area,
    strptime("fecha_actualizacion", '%Y-%m-%d')::DATE AS last_updated,
    "fecha_inicio"                                  AS start_period,
    "fecha_fin"                                     AS end_period
FROM "central-bank-of-peru-series"
