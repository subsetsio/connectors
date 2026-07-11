-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "region",
    "race_ethnicity",
    CAST("population_16_years_and_older" AS BIGINT) AS population_16_years_and_older,
    CAST("civilian_labor_force" AS BIGINT) AS civilian_labor_force,
    CAST("unemployed" AS BIGINT) AS unemployed,
    CAST("unemployment_rate" AS DOUBLE) AS unemployment_rate
FROM "new-york-state-department-of-labor-ykyj-hw45"
