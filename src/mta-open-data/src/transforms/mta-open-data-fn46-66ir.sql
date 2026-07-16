-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "day",
    "hour_of_promise_time",
    "provider_type",
    "pickup_borough",
    "trips",
    "ridership"
FROM "mta-open-data-fn46-66ir"
