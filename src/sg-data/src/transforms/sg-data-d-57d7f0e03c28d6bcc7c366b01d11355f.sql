-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "employment_size",
    "internet_usage"
FROM "sg-data-d-57d7f0e03c28d6bcc7c366b01d11355f"
