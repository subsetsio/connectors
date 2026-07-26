-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "leading_cause",
    "sex",
    "race_ethnicity",
    "deaths",
    "death_rate",
    "age_adjusted_death_rate"
FROM "nyc-open-data-jb7j-dtam"
