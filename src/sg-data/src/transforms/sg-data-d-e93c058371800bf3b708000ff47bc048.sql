-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "property_type",
    "category",
    "no_of_units"
FROM "sg-data-d-e93c058371800bf3b708000ff47bc048"
