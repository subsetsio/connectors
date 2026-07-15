-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "occupation",
    "retrench"
FROM "sg-data-d-a6246f522f3ea0cf265e3ef3ad59fe8e"
