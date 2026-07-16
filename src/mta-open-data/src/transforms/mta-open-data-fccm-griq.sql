-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "day_time",
    "delayed_trains",
    "on_time_trips",
    "on_time_performance",
    "delayed_trains_with_boat",
    "on_time_trips_with_boat",
    "on_time_performance_with",
    "scheduled_trips",
    "incomplete_trips",
    "trip_complete_percentage"
FROM "mta-open-data-fccm-griq"
