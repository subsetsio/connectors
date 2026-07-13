-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Pais" AS pais,
    CAST("Ano" AS BIGINT) AS ano,
    "Nombre_Indicador" AS nombre_indicador,
    "Fuente_General" AS fuente_general,
    "Fuente_Especifica" AS fuente_especifica,
    "Categoria" AS categoria,
    "Subcategoria1" AS subcategoria1,
    "Nivel_Educativo" AS nivel_educativo,
    "Tipo_Desagregacion" AS tipo_desagregacion,
    "Desagregacion" AS desagregacion,
    "Edades" AS edades,
    CAST("Valor" AS DOUBLE) AS valor,
    "source_resource"
FROM "idb-center-for-learning-improvement-information-cima-regional-indicators-2007-2"
