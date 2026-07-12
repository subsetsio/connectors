-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "level_of_education",
    "lmrhl_lt_lymy",
    "type_of_education",
    "nw_lt_lym",
    "gender",
    "lnw",
    "number_of_students_dd_ltlb"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-students-in-schools-and-universities-by-level-of-education-type-of"
