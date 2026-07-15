-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "total_paid_hours",
    "standard_hours"
FROM "sg-data-d-16c09eef57385fc29402ee71ffefd375"
