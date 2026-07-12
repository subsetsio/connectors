-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_education",
    "level_of_education_ar",
    "nationality",
    "nationality_ar",
    "gender",
    "gender_ar",
    "number_of_students"
FROM "qatar-planning-and-statistics-authority-special-needs-statistics-number-of-students-with-disabilities-integrated-into-public-schools-by"
