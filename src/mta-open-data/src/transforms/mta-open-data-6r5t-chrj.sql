-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "call_type",
    "number_of_calls_received",
    "number_of_calls_picked_up",
    "calls_answered",
    "average_answer_speed"
FROM "mta-open-data-6r5t-chrj"
