-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "year",
    "department",
    "job_group_description",
    "available_hours",
    "scheduled_overtime_hours",
    "paid_unavailable_hours",
    "unpaid_unavailable_hours",
    "annualized_availability"
FROM "mta-open-data-st8b-wj9a"
