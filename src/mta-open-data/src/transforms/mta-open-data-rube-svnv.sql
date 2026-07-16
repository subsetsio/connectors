-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "date",
    "hour_of_promise_time",
    "provider_type",
    "standard",
    "on_time_performance",
    "pickup_location",
    "total_pickups",
    "pickups_within_standards"
FROM "mta-open-data-rube-svnv"
