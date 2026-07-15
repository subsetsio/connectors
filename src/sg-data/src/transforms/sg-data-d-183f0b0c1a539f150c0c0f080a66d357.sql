-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "level_1",
    "level_2",
    "value"
FROM "sg-data-d-183f0b0c1a539f150c0c0f080a66d357"
