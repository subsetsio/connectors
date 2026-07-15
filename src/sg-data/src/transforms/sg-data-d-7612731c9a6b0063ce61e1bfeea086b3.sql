-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "size_of_trade_union",
    "no_of_trade_unions"
FROM "sg-data-d-7612731c9a6b0063ce61e1bfeea086b3"
