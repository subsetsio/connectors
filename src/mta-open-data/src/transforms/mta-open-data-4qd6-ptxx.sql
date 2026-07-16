-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "fleet_type",
    "mdbf_value",
    "fleet_owned",
    "no_of_primary_failures",
    "mdbf_goal",
    "no_of_primary_failures_goal"
FROM "mta-open-data-4qd6-ptxx"
