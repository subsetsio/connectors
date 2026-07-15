-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "actual_revised_estimated",
    "sector",
    "ministry",
    "type",
    "amount_in_millions",
    "percent_of_gdp"
FROM "sg-data-d-00f95040967791729d51bd7cd6af2355"
