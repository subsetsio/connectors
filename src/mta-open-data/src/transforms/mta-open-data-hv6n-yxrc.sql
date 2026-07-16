-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "peak_offpeak",
    "branch_id",
    "number_scheduled_trips",
    "number_trains_on_time",
    "percent_trains_on_time",
    "number_trains_3_to_6_min",
    "percent_trains_3_to_6_min",
    "number_trains_6_plus_min",
    "percent_trains_6_plus_min"
FROM "mta-open-data-hv6n-yxrc"
