-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row per series (the series dimension/catalog), not an observation table — join to central-bank-of-peru-values on codigo_serie to attach labels, unit and frequency to the observations.
SELECT
    "codigo_serie",
    "categoria",
    "grupo",
    "nombre",
    "descripcion",
    "geografia",
    "fuente",
    "frecuencia",
    "grupo_publicacion",
    "area_publica",
    strptime("fecha_actualizacion", '%Y-%m-%d')::DATE AS fecha_actualizacion,
    "fecha_inicio",
    "fecha_fin"
FROM "central-bank-of-peru-series"
