-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "category",
    CAST("year" AS BIGINT) AS year,
    "regions",
    "value"
FROM "geostat-environment-20statistics-forest-20resources-2-forest-planting-and-recovery"
