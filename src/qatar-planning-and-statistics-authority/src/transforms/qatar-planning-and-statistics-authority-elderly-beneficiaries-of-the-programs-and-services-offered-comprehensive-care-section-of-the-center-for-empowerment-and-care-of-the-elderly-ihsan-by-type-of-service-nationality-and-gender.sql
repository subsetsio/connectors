-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "nationality_ar",
    "permanent_host_males",
    "permanent_host_females",
    "hosting_intermittent_males",
    "hosting_intermittent_females",
    "hosting_for_a_limited_period_males",
    "hosting_for_a_limited_period_females"
FROM "qatar-planning-and-statistics-authority-elderly-beneficiaries-of-the-programs-and-services-offered-comprehensive-care-section-of-the-center-for-empowerment-and-care-of-the-elderly-ihsan-by-type-of-service-nationality-and-gender"
