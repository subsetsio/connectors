-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "occupation",
    "age",
    "employed"
FROM "sg-data-d-9392faa714d5e5809b07b10fbff2993e"
