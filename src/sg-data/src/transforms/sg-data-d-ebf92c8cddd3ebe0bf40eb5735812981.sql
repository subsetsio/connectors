-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age",
    "employment_rate"
FROM "sg-data-d-ebf92c8cddd3ebe0bf40eb5735812981"
