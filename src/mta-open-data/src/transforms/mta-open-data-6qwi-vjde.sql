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
    "actual_number_of_buses",
    "scheduled_number_of_buses",
    "service_delivered"
FROM "mta-open-data-6qwi-vjde"
