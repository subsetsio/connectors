-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_school",
    "nw_lmdrs",
    "gender",
    "ljns",
    "number_of_students"
FROM "qatar-planning-and-statistics-authority-number-of-students-in-private-schools-by-type-of-school-and-gender0"
