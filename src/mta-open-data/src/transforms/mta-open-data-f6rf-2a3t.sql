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
    "num_on_time_trips",
    "num_sched_trips",
    "terminal_on_time_performance"
FROM "mta-open-data-f6rf-2a3t"
