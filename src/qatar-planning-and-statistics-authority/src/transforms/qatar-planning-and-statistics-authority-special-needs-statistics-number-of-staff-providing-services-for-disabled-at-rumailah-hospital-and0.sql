-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "department",
    "gender",
    "number_of_staff",
    "gender_ar",
    "department_ar"
FROM "qatar-planning-and-statistics-authority-special-needs-statistics-number-of-staff-providing-services-for-disabled-at-rumailah-hospital-and0"
