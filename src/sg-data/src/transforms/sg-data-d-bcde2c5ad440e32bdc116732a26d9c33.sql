-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "applications_approved",
    "grants_disbursed"
FROM "sg-data-d-bcde2c5ad440e32bdc116732a26d9c33"
