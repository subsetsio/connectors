-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "demographics",
    "demographic_description",
    CAST("civilian_noninstitutional_population" AS BIGINT) AS civilian_noninstitutional_population,
    CAST("civilian_labor_force" AS BIGINT) AS civilian_labor_force,
    CAST("civilian_labor_force_as_a_percent_of_population" AS DOUBLE) AS civilian_labor_force_as_a_percent_of_population,
    CAST("employed" AS BIGINT) AS employed,
    CAST("employed_as_a_percent_of_population" AS DOUBLE) AS employed_as_a_percent_of_population,
    CAST("unemployed" AS BIGINT) AS unemployed,
    CAST("unemployed_as_a_percent_of_civilian_labor_force" AS DOUBLE) AS unemployed_as_a_percent_of_civilian_labor_force,
    CAST("not_in_labor_force" AS BIGINT) AS not_in_labor_force
FROM "new-york-state-department-of-labor-wkup-gbbg"
