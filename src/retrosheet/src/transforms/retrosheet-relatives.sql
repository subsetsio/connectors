-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source relationship list contains at least one exact duplicate relationship row, so it is published without a declared key.
SELECT
    "id1",
    "relation",
    "id2"
FROM "retrosheet-relatives"
