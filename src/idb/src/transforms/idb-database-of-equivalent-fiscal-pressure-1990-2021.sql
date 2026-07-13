-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Sheet" AS sheet,
    "Descripcion" AS descripcion,
    "source_resource"
FROM "idb-database-of-equivalent-fiscal-pressure-1990-2021"
