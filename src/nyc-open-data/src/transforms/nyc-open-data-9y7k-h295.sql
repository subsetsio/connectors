-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "created_year",
    "created_month",
    "additional_details",
    "total"
FROM "nyc-open-data-9y7k-h295"
