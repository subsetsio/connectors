-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "AREA" AS area,
    "CARRERA" AS carrera,
    "CIUDAD" AS ciudad,
    CAST("ANO" AS BIGINT) AS ano,
    "TIPO_DE_EDUCACION" AS tipo_de_educacion,
    CAST("MATRICULADOS_HOMBRES" AS BIGINT) AS matriculados_hombres,
    CAST("MATRICULADOS_MUJERES" AS BIGINT) AS matriculados_mujeres,
    CAST("NUEVOS_HOMBRES" AS BIGINT) AS nuevos_hombres,
    CAST("NUEVOS_MUJERES" AS BIGINT) AS nuevos_mujeres,
    CAST("TITULADOS_HOMBRES" AS BIGINT) AS titulados_hombres,
    CAST("TITULADOS_MUJERES" AS BIGINT) AS titulados_mujeres,
    "source_resource"
FROM "idb-dataset-of-universities-in-bolivia-supply-of-technical-and-professional-tra"
