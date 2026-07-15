-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "month",
    "date_of_retrieval_" AS date_of_retrieval,
    "operator",
    "plan",
    "max_speed",
    "plan_type",
    "connection_type",
    "contract_duration",
    "price_of_plan",
    "price_per_mbps"
FROM "sg-data-d-7a7f9510c00914869094fb466a2c9e04"
