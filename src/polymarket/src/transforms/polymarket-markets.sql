-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw market catalog can contain multiple snapshots of the same market across update times; use the latest-row transform when a one-row-per-market current catalog is needed.
-- caution: Binary Yes/No prices are only populated when the upstream outcomes decode to the standard Yes/No pair.
SELECT
    CAST("market_id" AS BIGINT) AS market_id,
    CAST("event_id" AS BIGINT) AS event_id,
    "event_slug",
    "event_title",
    "neg_risk",
    "question",
    "slug",
    "condition_id",
    "outcome_yes_price",
    "outcome_no_price",
    "volume_usd",
    "volume_24h_usd",
    "volume_1wk_usd",
    "volume_1mo_usd",
    "volume_1yr_usd",
    "liquidity_usd",
    "last_trade_price",
    "best_bid",
    "best_ask",
    "spread",
    "competitive",
    "is_active",
    "is_closed",
    "start_date",
    "end_date",
    "created_at",
    "updated_at"
FROM "polymarket-markets"
