-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cardholders",
    "bus_price",
    "train_price",
    "hybrid_price"
FROM "sg-data-d-b2d044a38a87a3f04d1802103b27f1bb"
