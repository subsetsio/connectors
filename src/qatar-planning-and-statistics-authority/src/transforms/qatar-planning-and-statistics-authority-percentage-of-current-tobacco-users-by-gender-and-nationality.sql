-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "percentage_of_current_female_tobacco_users",
    "percentage_of_current_male_tobacco_users",
    "overall_current_tobacco_users"
FROM "qatar-planning-and-statistics-authority-percentage-of-current-tobacco-users-by-gender-and-nationality"
