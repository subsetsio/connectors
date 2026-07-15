-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "day",
    "holiday"
FROM "sg-data-d-b773a1ad8dafa6ef27f4f2bf6a7c4a64"
