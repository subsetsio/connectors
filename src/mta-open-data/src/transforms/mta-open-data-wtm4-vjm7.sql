-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "trip_date",
    "peak_hour",
    "provider_type",
    "origin",
    "destination",
    "distance",
    "percent_of_scheduled_ride_time_category",
    "within_max_ride_time",
    "total_trips",
    "total_ride_time_min"
FROM "mta-open-data-wtm4-vjm7"
