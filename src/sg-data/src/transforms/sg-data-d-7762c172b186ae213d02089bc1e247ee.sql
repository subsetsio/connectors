-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "total_foreign_reserve_sgd",
    "special_drawing_rights",
    "imf_reserve_position",
    "gold_and_foreign_exchange",
    "total_foreign_reserve_usd"
FROM "sg-data-d-7762c172b186ae213d02089bc1e247ee"
