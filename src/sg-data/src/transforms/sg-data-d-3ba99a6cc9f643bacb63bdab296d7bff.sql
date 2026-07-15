-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "occupation",
    "employment_status",
    "employed"
FROM "sg-data-d-3ba99a6cc9f643bacb63bdab296d7bff"
