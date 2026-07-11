-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide small-business table; columns encode merchant and revenue measures by sector and income segment, so compare like-named measures rather than summing across all merchants_* and revenue_* columns.
SELECT
    "year",
    "month",
    "day_endofweek",
    "merchants_all",
    "revenue_all",
    "merchants_professional",
    "revenue_professional",
    "merchants_health",
    "revenue_health",
    "merchants_food_accommodation",
    "revenue_food_accommodation",
    "merchants_other_services",
    "revenue_other_services",
    "merchants_retail",
    "revenue_retail",
    "revenue_inclow",
    "merchants_inclow",
    "revenue_incmiddle",
    "merchants_incmiddle",
    "revenue_inchigh",
    "merchants_inchigh"
FROM "opportunity-insights-tracker-womply-national-weekly"
