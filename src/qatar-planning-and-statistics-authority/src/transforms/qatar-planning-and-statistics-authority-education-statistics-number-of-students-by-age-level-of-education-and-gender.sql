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
    "lnw",
    "number_of_students_dd_ltlb"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-students-by-age-level-of-education-and-gender"
