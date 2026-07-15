-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "work_week_pattern",
    "distribution"
FROM "sg-data-d-2c4005a1c24ab6bde1d2b762b8f64bec"
