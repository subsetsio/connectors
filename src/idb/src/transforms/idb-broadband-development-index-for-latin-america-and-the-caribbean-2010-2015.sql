-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Codigo" AS codigo,
    "Nombre_Variable" AS nombre_variable,
    "Unidad" AS unidad,
    "Fuente" AS fuente,
    "Descripcion" AS descripcion,
    CAST("Ano_Fecha" AS BIGINT) AS ano_fecha,
    CAST("Ano_Texto" AS BIGINT) AS ano_texto,
    "Pais_Nombre" AS pais_nombre,
    "Pais_Codigo" AS pais_codigo,
    CAST("Valor" AS DOUBLE) AS valor,
    "source_resource"
FROM "idb-broadband-development-index-for-latin-america-and-the-caribbean-2010-2015"
