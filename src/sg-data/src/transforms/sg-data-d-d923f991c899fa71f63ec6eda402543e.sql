-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "type_of_grounds",
    "amt_claim"
FROM "sg-data-d-d923f991c899fa71f63ec6eda402543e"
