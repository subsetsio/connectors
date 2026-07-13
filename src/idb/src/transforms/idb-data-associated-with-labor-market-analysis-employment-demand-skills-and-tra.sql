-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Hoja" AS hoja,
    "Nombre" AS nombre,
    "Contenido" AS contenido,
    "source_resource"
FROM "idb-data-associated-with-labor-market-analysis-employment-demand-skills-and-tra"
