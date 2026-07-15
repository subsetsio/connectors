-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "field_title",
    "description"
FROM "sg-data-d-1ebdc22551ae034d076722aa671e7f1b"
