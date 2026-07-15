-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "total",
    "short_work_week",
    "temporary_layoff"
FROM "sg-data-d-31d4c1a2de1f880c005dad945ff44d5d"
