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
    "number_of_teachers",
    "number_of_students",
    "number_of_classes",
    "number_of_schools"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-schools-classes-students-and-teachers-by-level-of-education-and-type"
