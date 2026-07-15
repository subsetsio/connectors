-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "constituency",
    "nomination_day",
    "polling_day"
FROM "sg-data-d-3ae9116b99b4bc1e64883f0d75aee967"
