-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no._awarded" AS no_awarded
FROM "sg-data-d-31f849c405eed919e41c29b234a5e7ad"
