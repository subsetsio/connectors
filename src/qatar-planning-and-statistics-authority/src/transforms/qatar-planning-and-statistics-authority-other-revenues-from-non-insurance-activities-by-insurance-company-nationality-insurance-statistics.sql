-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "particulars_ar",
    "particulars",
    "nationality_of_insurance_company_ar",
    "nationality_of_insurance_company",
    "value"
FROM "qatar-planning-and-statistics-authority-other-revenues-from-non-insurance-activities-by-insurance-company-nationality-insurance-statistics"
