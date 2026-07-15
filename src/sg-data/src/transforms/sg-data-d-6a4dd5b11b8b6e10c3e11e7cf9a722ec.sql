-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "volume_of_sms"
FROM "sg-data-d-6a4dd5b11b8b6e10c3e11e7cf9a722ec"
