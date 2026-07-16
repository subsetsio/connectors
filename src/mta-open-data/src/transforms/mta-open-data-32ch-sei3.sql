-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "division",
    "line",
    "day_type",
    "num_sched_trains",
    "num_actual_trains",
    "service_delivered"
FROM "mta-open-data-32ch-sei3"
