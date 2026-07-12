-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "job_title",
    "lmsm_lwzyfy",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "number_of_staff"
FROM "qatar-planning-and-statistics-authority-number-of-teaching-and-administrative-staff-in-private-schools-by-job-title-nationality-and-gender0"
