-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "town",
    "room_type",
    "min_selling_price",
    "max_selling_price",
    "min_selling_price_less_ahg_shg",
    "max_selling_price_less_ahg_shg"
FROM "sg-data-d-2d493bdcc1d9a44828b6e71cb095b88d"
