-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_education",
    "level_of_education_ar",
    "type_of_school",
    "type_of_school_ar",
    "nationality",
    "nationality_ar",
    "gender",
    "gender_ar",
    "number_of_students"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-students-in-private-schools-by-level-of-education-type-of-school"
