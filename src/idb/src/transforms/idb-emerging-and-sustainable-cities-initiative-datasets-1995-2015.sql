-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("IndicadorId" AS BIGINT) AS indicadorid,
    "CiudadId" AS ciudadid,
    "Fuente" AS fuente,
    "Source" AS source,
    CAST("Anio" AS BIGINT) AS anio,
    "Valor" AS valor,
    "source_resource"
FROM "idb-emerging-and-sustainable-cities-initiative-datasets-1995-2015"
