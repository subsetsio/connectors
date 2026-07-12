-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes a synthetic ecosystem aggregate row series alongside project-level series; filter it out before summing across projects.
SELECT
    "project_slug",
    "timestamp",
    "date",
    "tx_count",
    "uops_count"
FROM "l2beat-activity"
