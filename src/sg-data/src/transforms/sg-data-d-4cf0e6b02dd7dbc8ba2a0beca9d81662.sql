-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "amt_of_loans_granted"
FROM "sg-data-d-4cf0e6b02dd7dbc8ba2a0beca9d81662"
