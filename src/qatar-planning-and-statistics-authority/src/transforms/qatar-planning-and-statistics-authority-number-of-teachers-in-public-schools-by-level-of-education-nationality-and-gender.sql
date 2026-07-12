-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_education",
    "nationality",
    "gender",
    "number_of_teachers",
    "gender_ar",
    "nationality_ar",
    "educational_level_ar"
FROM "qatar-planning-and-statistics-authority-number-of-teachers-in-public-schools-by-level-of-education-nationality-and-gender"
