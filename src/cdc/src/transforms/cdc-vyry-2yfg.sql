-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "old_url",
    "new_url",
    CAST("is_primary" AS BOOLEAN) AS is_primary
FROM "cdc-vyry-2yfg"
