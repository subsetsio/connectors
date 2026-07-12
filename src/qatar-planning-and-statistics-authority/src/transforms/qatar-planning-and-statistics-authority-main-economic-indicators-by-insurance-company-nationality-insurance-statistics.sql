-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "jnsy_shrk_lt_myn",
    "nationality_of_insurance_company",
    "lmw_shr",
    "indicator",
    "value"
FROM "qatar-planning-and-statistics-authority-main-economic-indicators-by-insurance-company-nationality-insurance-statistics"
