-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "academic_year",
    "category",
    "lfy",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-public-schools-teaching-and-administrative-staff-by-nationality-gender-and-level-of-education"
