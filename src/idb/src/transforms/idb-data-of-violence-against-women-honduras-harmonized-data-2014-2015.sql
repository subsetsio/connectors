-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Pais" AS pais,
    "Categoria" AS categoria,
    "Indicador" AS indicador,
    "Sub-indicador" AS sub_indicador,
    "Respuesta" AS respuesta,
    CAST("Valor" AS BIGINT) AS valor,
    CAST("Porcentaje" AS DOUBLE) AS porcentaje,
    "source_resource"
FROM "idb-data-of-violence-against-women-honduras-harmonized-data-2014-2015"
