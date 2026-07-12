-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "educational_institution",
    "educational_institution_ar",
    "gender",
    "gender_ar",
    "number_of_new_students"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-new-students-on-scholarships-at-universities-and-colleges-inside"
