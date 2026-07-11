-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "day_endofweek",
    "cityid",
    "merchants_all",
    "revenue_all"
FROM "opportunity-insights-tracker-womply-city-weekly"
