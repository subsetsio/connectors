-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_group",
    "nationality",
    "percentage_of_female_tobacco_users",
    "percentage_of_male_tobacco_users",
    "overall_tobacco_users_percentage"
FROM "qatar-planning-and-statistics-authority-percentage-of-tobacco-users-by-age-group-nationality-and-gender"
