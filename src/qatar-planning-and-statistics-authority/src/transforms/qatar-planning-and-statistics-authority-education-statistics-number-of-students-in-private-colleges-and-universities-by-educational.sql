-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "educational_institution",
    "educational_institution_ar",
    "nationality",
    "nationality_ar",
    "gender",
    "gender_ar",
    "number_of_students"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-students-in-private-colleges-and-universities-by-educational"
