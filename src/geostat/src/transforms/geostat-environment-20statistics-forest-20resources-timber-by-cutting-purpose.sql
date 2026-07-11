-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "forest_type",
    CAST("year" AS BIGINT) AS year,
    "cutting_purpose",
    "value"
FROM "geostat-environment-20statistics-forest-20resources-timber-by-cutting-purpose"
