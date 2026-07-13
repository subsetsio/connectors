-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "IndicadorNombre_EN" AS indicadornombre_en,
    "IndicadorNombre_ES" AS indicadornombre_es,
    "Indicador_Nombre_PT" AS indicador_nombre_pt,
    "Pais_Nombre_EN" AS pais_nombre_en,
    "PaisNombre_ES" AS paisnombre_es,
    CAST("Ano" AS BIGINT) AS ano,
    CAST("Valor" AS DOUBLE) AS valor,
    "FuenteDescripcion_EN" AS fuentedescripcion_en,
    "Fuente_Descripcion_ES" AS fuente_descripcion_es,
    "Nota_Descripcion_EN" AS nota_descripcion_en,
    "Nota_Descripcion_ES" AS nota_descripcion_es,
    "source_resource"
FROM "idb-tables-and-figures-for-revenue-collection-is-not-enough-taxes-as-an-instrum"
