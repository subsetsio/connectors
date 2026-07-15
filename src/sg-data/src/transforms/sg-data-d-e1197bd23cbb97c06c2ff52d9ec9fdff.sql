-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "employment_status",
    "age",
    "employed"
FROM "sg-data-d-e1197bd23cbb97c06c2ff52d9ec9fdff"
