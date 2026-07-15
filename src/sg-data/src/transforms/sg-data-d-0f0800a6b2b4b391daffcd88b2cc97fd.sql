-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_balance",
    "actual_revised_estimated",
    "category",
    "item",
    "amount_in_millions",
    "percent_of_GDP" AS percent_of_gdp
FROM "sg-data-d-0f0800a6b2b4b391daffcd88b2cc97fd"
