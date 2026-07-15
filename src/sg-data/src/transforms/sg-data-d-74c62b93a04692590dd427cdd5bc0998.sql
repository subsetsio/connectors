-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "sub_sector",
    "number_of_electricity_accounts"
FROM "sg-data-d-74c62b93a04692590dd427cdd5bc0998"
