-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "lbldy",
    "level_of_education",
    "lmrhl_lt_lymy",
    "type_of_school",
    "nw_lmdrs",
    "number_of_students",
    "number_of_schools"
FROM "qatar-planning-and-statistics-authority-number-of-public-schools-and-their-students-by-municipality-level-of-education-and-type-of-school"
