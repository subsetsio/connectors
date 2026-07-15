-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "total",
    "short_work_week",
    "temporary_layoff"
FROM "sg-data-d-46b49c3bf00d87eaa24441f339387467"
