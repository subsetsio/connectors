-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "cost_per_dollar_of_tax_collected"
FROM "sg-data-d-697b2ff8c060349260a2645fb36a9cf8"
