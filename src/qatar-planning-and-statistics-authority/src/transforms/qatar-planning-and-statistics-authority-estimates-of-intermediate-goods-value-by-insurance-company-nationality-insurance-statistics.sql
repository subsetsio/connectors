-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality_of_insurance_company",
    "lmstlzmt_lsl_y",
    "goods",
    "value"
FROM "qatar-planning-and-statistics-authority-estimates-of-intermediate-goods-value-by-insurance-company-nationality-insurance-statistics"
