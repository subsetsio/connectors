-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "female_average_age_of_daily_smoking_initiation",
    "male_average_age_of_daily_smoking_initiation",
    "overall_average_age_of_daily_smoking_initiation"
FROM "qatar-planning-and-statistics-authority-average-age-of-daily-smoking-initiation-by-gender"
