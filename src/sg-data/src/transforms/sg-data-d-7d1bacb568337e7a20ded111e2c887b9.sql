-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "operators",
    "call_success_rate"
FROM "sg-data-d-7d1bacb568337e7a20ded111e2c887b9"
