-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "percent_of_annual_receipts_by_donations",
    "percent_of_annual_receipts_by_govt_grants",
    "percent_of_annual_receipts_by_others"
FROM "sg-data-d-d2b0ae25e9dc329dd3a8de8535858390"
