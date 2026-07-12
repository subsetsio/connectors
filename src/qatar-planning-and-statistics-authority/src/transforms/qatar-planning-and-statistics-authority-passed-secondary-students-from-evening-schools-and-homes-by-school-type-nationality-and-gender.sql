-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_school",
    "nw_lmdrs",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "number_of_passed_students"
FROM "qatar-planning-and-statistics-authority-passed-secondary-students-from-evening-schools-and-homes-by-school-type-nationality-and-gender"
