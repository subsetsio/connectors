-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "professional_status",
    "llqb_ljm_y",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-teaching-and-administrative-staff-of-private-colleges-and-universities-by-gender-nationality-and"
