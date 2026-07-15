-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "value_of_purchase",
    "percentage"
FROM "sg-data-d-79958154e6f9d9a30c5655ddd41d83c5"
