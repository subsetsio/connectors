-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "day",
    "month",
    "year",
    "daily_spend_19_all",
    "daily_spend_19_q1",
    "daily_spend_19_q2",
    "daily_spend_19_q3",
    "daily_spend_19_q4"
FROM "opportunity-insights-tracker-affinity-daily-total-spending-national"
