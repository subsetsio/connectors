-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "day_endofweek",
    "cityid",
    "engagement",
    "badges",
    "break_engagement",
    "break_badges"
FROM "opportunity-insights-tracker-zearn-city-weekly"
