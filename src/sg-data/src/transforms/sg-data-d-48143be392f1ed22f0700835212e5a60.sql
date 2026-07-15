-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "type_of_hdb",
    "no_of_cases",
    "median_annual_value",
    "property_tax_collection"
FROM "sg-data-d-48143be392f1ed22f0700835212e5a60"
