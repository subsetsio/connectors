-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "property_type",
    "no_of_cases",
    "annual_value",
    "median_annual_value",
    "property_tax_collection"
FROM "sg-data-d-e96a2e27e7d3c35bb167068844ca0210"
