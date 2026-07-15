-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "occupation",
    "total",
    "short_work_week",
    "temporary_layoff"
FROM "sg-data-d-6e31884107e528965607fed92094384c"
