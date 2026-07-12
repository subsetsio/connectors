-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_school",
    "job_title",
    "gender",
    "number_of_staff",
    "gender_ar",
    "job_title_ar",
    "type_of_school_ar"
FROM "qatar-planning-and-statistics-authority-private-schools-teaching-and-administrative-staff-by-type-of-school-and-gender"
