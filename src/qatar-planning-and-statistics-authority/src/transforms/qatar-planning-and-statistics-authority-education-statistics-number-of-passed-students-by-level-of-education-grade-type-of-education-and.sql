-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_education",
    "level_of_education_ar",
    "grade",
    "grade_ar",
    "type_of_education",
    "type_of_education_ar",
    "gender",
    "gender_ar",
    "number_of_passed_students_dd_ltlb_lnjhyn",
    "number_of_registered_students_dd_ltlb_lmsjlyn"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-passed-students-by-level-of-education-grade-type-of-education-and"
