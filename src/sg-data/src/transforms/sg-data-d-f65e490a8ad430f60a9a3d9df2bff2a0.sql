-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "market_segment",
    "price_index"
FROM "sg-data-d-f65e490a8ad430f60a9a3d9df2bff2a0"
