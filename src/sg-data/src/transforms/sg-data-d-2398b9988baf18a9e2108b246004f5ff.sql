-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "industry",
    "total",
    "short_work_week",
    "temporary_layoff"
FROM "sg-data-d-2398b9988baf18a9e2108b246004f5ff"
