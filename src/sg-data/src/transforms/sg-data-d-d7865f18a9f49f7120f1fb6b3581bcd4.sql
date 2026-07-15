-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "address",
    "vaccine"
FROM "sg-data-d-d7865f18a9f49f7120f1fb6b3581bcd4"
