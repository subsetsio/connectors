-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "currency_code",
    "unit",
    "date",
    "buying_rate",
    "selling_rate",
    "middle_rate"
FROM "bank-negara-malaysia-exchange-rate"
