-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_school",
    "type_of_school_ar",
    "gender",
    "gender_ar",
    "number_of_students_dd_ltlb"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-students-in-private-schools-by-type-of-school-and-gender"
