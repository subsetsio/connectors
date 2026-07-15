-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "age1",
    "reentry_rate_12mth"
FROM "sg-data-d-4fa5204237e205316b2be6888ebd5990"
