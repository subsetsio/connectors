-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "age_group",
    "perceived_availability_of_state_support",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-nh27.px"
