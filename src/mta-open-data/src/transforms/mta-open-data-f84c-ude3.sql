-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "date",
    "hour_of_promise_time",
    "provider_type",
    "arrival_time",
    "_30minearlyto1late" AS 30minearlyto1late,
    "pickup_location",
    "total_appointment_trips",
    "trips_within_arrival_time"
FROM "mta-open-data-f84c-ude3"
