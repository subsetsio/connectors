-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "transit_timestamp",
    "bus_route",
    "payment_method",
    "fare_class_category",
    "ridership",
    "transfers"
FROM "mta-open-data-kv7t-n8in"
