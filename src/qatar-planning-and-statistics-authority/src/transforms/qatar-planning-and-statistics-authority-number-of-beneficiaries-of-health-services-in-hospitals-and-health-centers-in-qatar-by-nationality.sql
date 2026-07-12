-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nationality",
    "nationality_ar",
    "year",
    "health_centers",
    "hospitals"
FROM "qatar-planning-and-statistics-authority-number-of-beneficiaries-of-health-services-in-hospitals-and-health-centers-in-qatar-by-nationality"
