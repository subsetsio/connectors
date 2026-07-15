-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "claim_items",
    "number_of_claims"
FROM "sg-data-d-f5d9209c996b9d9fc6c2a781aa23fcbf"
