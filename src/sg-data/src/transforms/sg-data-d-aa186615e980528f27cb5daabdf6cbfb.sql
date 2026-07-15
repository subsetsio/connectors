-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "size_of_trade_union",
    "no_of_members"
FROM "sg-data-d-aa186615e980528f27cb5daabdf6cbfb"
