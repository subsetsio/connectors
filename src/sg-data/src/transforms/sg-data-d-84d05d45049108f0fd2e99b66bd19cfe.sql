-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "market_segment",
    "completion_status",
    "launch_status",
    "pre_requisites_status",
    "units"
FROM "sg-data-d-84d05d45049108f0fd2e99b66bd19cfe"
