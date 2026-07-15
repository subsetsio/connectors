-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "age",
    "highest_qualification_attained",
    "nsa_unemployment_rate"
FROM "sg-data-d-79699e0bd51d2d8cee7fb3f6d29dc7c4"
