-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age",
    "l_mr",
    "level_of_education",
    "lmrhl_lt_lymy",
    "gender",
    "ljns",
    "number_of_students"
FROM "qatar-planning-and-statistics-authority-number-of-students-by-age-level-of-education-and-gender"
