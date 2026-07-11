-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "day_endofweek",
    "countyfips",
    "engagement",
    "badges",
    "break_engagement",
    "break_badges",
    "imputed_from_cz"
FROM "opportunity-insights-tracker-zearn-county-weekly"
