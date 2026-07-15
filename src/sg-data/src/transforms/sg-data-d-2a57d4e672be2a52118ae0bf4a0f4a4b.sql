-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sn",
    "medication",
    "subsidy"
FROM "sg-data-d-2a57d4e672be2a52118ae0bf4a0f4a4b"
