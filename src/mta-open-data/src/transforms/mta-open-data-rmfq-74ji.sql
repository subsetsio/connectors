-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "date",
    "hour_of_promise_time",
    "provider_type",
    "percentage_of_trips_within",
    "pick_up_location",
    "total_appointment_trips",
    "dropoffs_within_standard"
FROM "mta-open-data-rmfq-74ji"
