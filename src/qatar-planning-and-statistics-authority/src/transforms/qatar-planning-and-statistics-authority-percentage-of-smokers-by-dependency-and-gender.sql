-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_dependency",
    "percentage_of_female_users",
    "percentage_of_male_users",
    "overall_percentage"
FROM "qatar-planning-and-statistics-authority-percentage-of-smokers-by-dependency-and-gender"
