-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "university_title",
    "nationality",
    "gender",
    "number_of_staff",
    "gender_ar",
    "nationality_ar",
    "university_title_ar"
FROM "qatar-planning-and-statistics-authority-teaching-and-administrative-staff-of-private-colleges-and-universities-by-university-title-nationality-and-gender"
