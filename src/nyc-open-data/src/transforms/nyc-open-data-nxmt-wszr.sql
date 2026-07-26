-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_ending_weekly_starting_on_sundays",
    "number_of_sessions",
    "average_session_length",
    "number_of_unique_clients",
    "tb_downloaded",
    "tb_uploaded",
    "cumulative_bandwidth_utilization_to_date_tb",
    "cumulative_sessions_to_date",
    "cumulative_subscribers_to_date"
FROM "nyc-open-data-nxmt-wszr"
