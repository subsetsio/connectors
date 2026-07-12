-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_education",
    "lmrhl_lt_lymy",
    "gender",
    "ljns",
    "type_of_education",
    "nw_lt_lym",
    "number_of_teachers",
    "number_of_students"
FROM "qatar-planning-and-statistics-authority-number-of-students-and-teachers-in-schools-by-level-of-education-gender-and-type-of-education"
