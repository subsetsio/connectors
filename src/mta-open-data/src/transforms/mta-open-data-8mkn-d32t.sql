-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "borough",
    "trip_type",
    "route_id",
    "period",
    "number_of_customers",
    "additional_bus_stop_time",
    "additional_travel_time",
    "customer_journey_time"
FROM "mta-open-data-8mkn-d32t"
