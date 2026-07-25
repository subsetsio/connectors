-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("state" AS BIGINT) AS state,
    CAST("local" AS BIGINT) AS local,
    CAST("federal" AS BIGINT) AS federal
FROM "u-s-department-of-transportation-9pk4-tjjw"
