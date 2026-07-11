-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicator" AS indicator,
    "Industry classification" AS industry_classification,
    "Loan type" AS loan_type,
    "Quarter" AS quarter,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0700-035v1"
