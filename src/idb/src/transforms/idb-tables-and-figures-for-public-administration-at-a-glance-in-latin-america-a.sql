-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Pais" AS pais,
    "Codigo_Pais" AS codigo_pais,
    CAST("Ano" AS BIGINT) AS ano,
    "Indicador" AS indicador,
    CAST("Valor" AS DOUBLE) AS valor,
    "Medida" AS medida,
    CAST("Ano_Fecha" AS BIGINT) AS ano_fecha,
    "source_resource"
FROM "idb-tables-and-figures-for-public-administration-at-a-glance-in-latin-america-a"
