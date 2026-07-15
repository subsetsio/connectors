-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age",
    "no_minimum_protection",
    "minimum_protection"
FROM "sg-data-d-5f9b504acdd7ebc298a974117b490435"
