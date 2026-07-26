-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_week" AS week,
    "sessions_per_week",
    "cumulative_sessions_to_date",
    "bandwidth_utilization_per_week_tb",
    "cumulative_bandwidth_utilization_to_date_tb",
    "average_session_duration",
    "new_subscribers_per_week",
    "total_subscribers_per_week",
    "cumulative_subscribers_to_date"
FROM "nyc-open-data-69wu-b929"
