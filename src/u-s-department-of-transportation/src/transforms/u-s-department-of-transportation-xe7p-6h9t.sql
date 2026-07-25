-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    CAST("passengers" AS DOUBLE) AS passengers,
    CAST("vehicles" AS DOUBLE) AS vehicles,
    CAST("year" AS BIGINT) AS year
FROM "u-s-department-of-transportation-xe7p-6h9t"
