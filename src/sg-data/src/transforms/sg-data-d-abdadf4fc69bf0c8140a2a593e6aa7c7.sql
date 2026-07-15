-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "operating_expenditure",
    "development_expenditure",
    "government_health_expenditure",
    "percentage_gdp"
FROM "sg-data-d-abdadf4fc69bf0c8140a2a593e6aa7c7"
