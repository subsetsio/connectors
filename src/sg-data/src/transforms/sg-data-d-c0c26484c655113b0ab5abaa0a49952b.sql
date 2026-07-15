-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "level_1",
    "level_2",
    "value"
FROM "sg-data-d-c0c26484c655113b0ab5abaa0a49952b"
