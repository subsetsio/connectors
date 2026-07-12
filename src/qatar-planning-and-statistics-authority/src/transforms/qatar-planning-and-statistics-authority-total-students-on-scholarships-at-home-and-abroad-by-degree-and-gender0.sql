-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "level_of_education",
    "nationality",
    "gender",
    "number_of_teachers_dd_lmdrsyn",
    "lnw",
    "ljnsy",
    "lmrhl_lt_lymy"
FROM "qatar-planning-and-statistics-authority-total-students-on-scholarships-at-home-and-abroad-by-degree-and-gender0"
