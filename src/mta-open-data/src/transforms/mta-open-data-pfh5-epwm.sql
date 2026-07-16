-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "agency",
    "department",
    "rc",
    "rc_name",
    "job_group_description",
    "availability_type",
    "availability_subtype",
    "total_hours"
FROM "mta-open-data-pfh5-epwm"
