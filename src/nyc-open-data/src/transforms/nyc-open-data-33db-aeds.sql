-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "cash_assistance_medical_assistance",
    "supplemental_security_income_medical_assistance",
    "nursing_home_medical_assistance",
    "medical_assistance_only",
    "total_hraenrolled_medical_assistance_individuals"
FROM "nyc-open-data-33db-aeds"
