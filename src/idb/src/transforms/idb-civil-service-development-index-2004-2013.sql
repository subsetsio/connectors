-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Pais" AS pais,
    CAST("Ano" AS BIGINT) AS ano,
    "Categoria_Indicador" AS categoria_indicador,
    "Nombre_Indicador" AS nombre_indicador,
    CAST("Puntaje" AS BIGINT) AS puntaje,
    "source_resource"
FROM "idb-civil-service-development-index-2004-2013"
