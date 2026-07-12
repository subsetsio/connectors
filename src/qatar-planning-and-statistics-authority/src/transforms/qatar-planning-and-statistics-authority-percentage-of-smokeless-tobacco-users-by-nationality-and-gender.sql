-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_smokeless_tobacco_users",
    "nationality",
    "of_female_users",
    "of_male_users",
    "total"
FROM "qatar-planning-and-statistics-authority-percentage-of-smokeless-tobacco-users-by-nationality-and-gender"
