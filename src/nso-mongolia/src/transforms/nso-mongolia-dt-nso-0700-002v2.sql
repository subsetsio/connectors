-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Loan classification" AS loan_classification,
    "Sectors" AS sectors,
    strptime("Month", '%Y-%m')::DATE AS month,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0700-002v2"
