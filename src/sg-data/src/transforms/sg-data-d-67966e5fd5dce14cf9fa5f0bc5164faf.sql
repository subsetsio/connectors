-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "property_type",
    "category",
    "flat_type",
    "no_of_units"
FROM "sg-data-d-67966e5fd5dce14cf9fa5f0bc5164faf"
