-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row carries buying and selling prices for multiple coin weights; reshape by coin weight and side before aggregating prices.
SELECT
    "date",
    "one_oz_buying",
    "one_oz_selling",
    "half_oz_buying",
    "half_oz_selling",
    "quarter_oz_buying",
    "quarter_oz_selling"
FROM "bank-negara-malaysia-kijang-emas"
