-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activities",
    "activities_ar",
    "activities_beneficiaries",
    "activities_beneficiaries_ar",
    "count"
FROM "qatar-planning-and-statistics-authority-activities-rendered-by-the-family-consulting-center-and-number-of-beneficiaries"
