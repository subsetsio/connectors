-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "jnsy_shrk_lt_myn",
    "nationality_of_insurance_company",
    "mw_shr",
    "indicator",
    "jnsy",
    "nationality",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-employees-and-estimated-compensation-by-nationality-and-insurance-company-nationality0"
