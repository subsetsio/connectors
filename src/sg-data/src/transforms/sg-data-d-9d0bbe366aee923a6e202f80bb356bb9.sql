-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hospital",
    "minutes"
FROM "sg-data-d-9d0bbe366aee923a6e202f80bb356bb9"
