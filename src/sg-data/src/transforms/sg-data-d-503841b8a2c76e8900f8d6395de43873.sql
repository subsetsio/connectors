-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "actual_revised_estimated",
    "fund",
    "amount"
FROM "sg-data-d-503841b8a2c76e8900f8d6395de43873"
