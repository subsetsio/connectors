-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "income_size",
    "proportion_of_annual_receipts"
FROM "sg-data-d-b36163ca340f3d1c3e7bd3ca01566973"
