-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "region",
    CAST("youth_population" AS BIGINT) AS youth_population,
    CAST("youth_civilian_labor_force" AS BIGINT) AS youth_civilian_labor_force,
    CAST("youth_unemployed" AS BIGINT) AS youth_unemployed,
    CAST("youth_unemployment_rate" AS DOUBLE) AS youth_unemployment_rate
FROM "new-york-state-department-of-labor-rrw8-ncwn"
