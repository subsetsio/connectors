-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "mean_sunshine_hrs"
FROM "sg-data-d-9a80d732aa5de0a68be0557fc9437ad0"
