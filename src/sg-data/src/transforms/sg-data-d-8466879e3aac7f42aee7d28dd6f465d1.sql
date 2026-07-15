-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "telco",
    "drop_call_rate"
FROM "sg-data-d-8466879e3aac7f42aee7d28dd6f465d1"
