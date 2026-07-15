-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "source",
    "sector",
    "annual_receipts"
FROM "sg-data-d-681b5b86959cfd1795764ca4944e6884"
