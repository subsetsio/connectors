-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "town_or_estate",
    "flat_type",
    "sold_or_rental",
    "no_of_dwelling_units"
FROM "sg-data-d-07b1eeeb22efdf7faf5bd6a13667359d"
