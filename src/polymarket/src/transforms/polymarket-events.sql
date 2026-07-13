-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Events are grouping records for related markets; event-level volume and liquidity should not be summed together with market-level volume without choosing the intended aggregation level.
SELECT
    CAST("event_id" AS BIGINT) AS event_id,
    "ticker",
    "slug",
    "title",
    "category",
    "description",
    "volume_usd",
    "volume_24h_usd",
    "volume_1wk_usd",
    "volume_1mo_usd",
    "volume_1yr_usd",
    "liquidity_usd",
    "open_interest",
    "comment_count",
    "competitive",
    "neg_risk",
    "is_active",
    "is_closed",
    "is_archived",
    "is_featured",
    "is_restricted",
    "market_count",
    "start_date",
    "end_date",
    "creation_date",
    CAST("created_at" AS TIMESTAMP) AS created_at,
    "updated_at"
FROM "polymarket-events"
