-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "update_date",
    "project_id",
    "acep",
    "current_budget",
    "baseline_budget",
    "expenditures",
    "task",
    "annotations"
FROM "mta-open-data-f6fd-xfps"
