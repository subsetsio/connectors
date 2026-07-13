-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "None" AS none,
    "Hoja" AS hoja,
    "Titulo_tablas" AS titulo_tablas,
    "source_resource"
FROM "idb-bolivia-labor-market-survey-demand-2022-aggregated-data"
