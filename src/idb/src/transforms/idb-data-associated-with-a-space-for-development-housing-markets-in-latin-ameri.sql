-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicador_Nombre_EN" AS indicador_nombre_en,
    "Indicador_Nombre_ES" AS indicador_nombre_es,
    "Indicador_Nombre_PT" AS indicador_nombre_pt,
    "Pais_Nombre_EN" AS pais_nombre_en,
    "Pais_Nombre_ES" AS pais_nombre_es,
    CAST("Ano" AS BIGINT) AS ano,
    CAST("Valor" AS DOUBLE) AS valor,
    "Fuente_Descripcion_EN" AS fuente_descripcion_en,
    "Fuente_Descripcion_ES" AS fuente_descripcion_es,
    "Nota_Descripcion_EN" AS nota_descripcion_en,
    "Nota_Descripcion_ES" AS nota_descripcion_es,
    "source_resource"
FROM "idb-data-associated-with-a-space-for-development-housing-markets-in-latin-ameri"
