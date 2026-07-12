-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_tobacco_smokers",
    "nationality",
    "of_female_users",
    "of_male_users",
    "overall"
FROM "qatar-planning-and-statistics-authority-percentage-of-tobacco-smokers-by-type-of-smoker-nationality-and-gender"
