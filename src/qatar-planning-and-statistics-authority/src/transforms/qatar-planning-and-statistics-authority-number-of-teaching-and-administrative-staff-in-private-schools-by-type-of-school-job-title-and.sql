-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_school",
    "nw_lmdrs",
    "job_title",
    "lmsm_lwzyfy",
    "gender",
    "ljns",
    "number_of_staff"
FROM "qatar-planning-and-statistics-authority-number-of-teaching-and-administrative-staff-in-private-schools-by-type-of-school-job-title-and"
