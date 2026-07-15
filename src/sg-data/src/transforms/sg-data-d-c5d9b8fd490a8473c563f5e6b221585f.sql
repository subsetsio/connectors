-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name",
    "address",
    "vaccine"
FROM "sg-data-d-c5d9b8fd490a8473c563f5e6b221585f"
