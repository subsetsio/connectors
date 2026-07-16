-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "borough",
    "day_type",
    "trip_type",
    "route_id",
    "period",
    "number_of_trips_passing_wait",
    "number_of_scheduled_trips",
    "wait_assessment"
FROM "mta-open-data-v4z4-2h6n"
