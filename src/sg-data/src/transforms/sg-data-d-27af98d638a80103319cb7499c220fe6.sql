-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "flat_type",
    "resale_transactions"
FROM "sg-data-d-27af98d638a80103319cb7499c220fe6"
