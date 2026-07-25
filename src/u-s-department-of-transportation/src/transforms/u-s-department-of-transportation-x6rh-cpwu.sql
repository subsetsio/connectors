-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("date" AS TIMESTAMP) AS date,
    CAST("monthly_teu_capacity" AS BIGINT) AS monthly_teu_capacity
FROM "u-s-department-of-transportation-x6rh-cpwu"
