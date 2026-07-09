-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    CAST("lower_ci" AS DOUBLE) AS lower_ci,
    CAST("upper_ci" AS DOUBLE) AS upper_ci,
    "two_year_intervals",
    "time",
    "administrative_geography",
    "geography",
    "sex",
    "sex_1",
    "age_groups",
    "agegroups"
FROM "ons-life-expectancy-by-local-authority"
