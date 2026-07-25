-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("total_calls" AS BIGINT) AS total_calls,
    CAST("total_number_of_passengers" AS BIGINT) AS total_number_of_passengers
FROM "u-s-department-of-transportation-uxyn-8v2z"
