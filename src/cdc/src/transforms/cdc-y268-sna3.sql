-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "State" AS state,
    "Age Group (Years)" AS age_group_years,
    CAST("State Rate" AS DOUBLE) AS state_rate,
    CAST("State Births" AS BIGINT) AS state_births,
    CAST("U.S. Births" AS BIGINT) AS u_s_births,
    CAST("U.S. Birth Rate" AS DOUBLE) AS u_s_birth_rate,
    "Unit" AS unit
FROM "cdc-y268-sna3"
