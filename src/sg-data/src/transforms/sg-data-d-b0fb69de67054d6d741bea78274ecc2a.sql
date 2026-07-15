-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "temp_mean_daily_max"
FROM "sg-data-d-b0fb69de67054d6d741bea78274ecc2a"
