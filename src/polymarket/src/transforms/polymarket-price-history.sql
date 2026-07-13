-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Price history is scoped to high-volume binary markets selected from the markets catalog, not every market on Polymarket.
-- caution: The price column is the Yes outcome probability at the sampled timestamp.
SELECT
    CAST("market_id" AS BIGINT) AS market_id,
    "timestamp",
    CAST(to_timestamp("timestamp") AS TIMESTAMP) AS datetime,
    "price"
FROM "polymarket-price-history"
