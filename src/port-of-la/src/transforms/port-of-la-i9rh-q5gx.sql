-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("dry_bulk" AS DOUBLE) AS dry_bulk,
    CAST("liquid_bulk" AS DOUBLE) AS liquid_bulk,
    CAST("general_cargo" AS DOUBLE) AS general_cargo,
    CAST("total" AS DOUBLE) AS total
FROM "port-of-la-i9rh-q5gx"
