-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "date",
    "ulsd_gallons_hedged",
    "percent_of_expected_ulsd_gallons_purchased",
    "weighted_average_hedge_price_per_month",
    "current_adopted_budget_forecasted_commodity_price",
    "posted_date"
FROM "mta-open-data-dips-jfpb"
