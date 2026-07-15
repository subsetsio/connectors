-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "type_of_private_residential",
    "no_of_cases",
    "median_annual_value",
    "property_tax_collection"
FROM "sg-data-d-774a81df45dca33112e59207e6dae1af"
