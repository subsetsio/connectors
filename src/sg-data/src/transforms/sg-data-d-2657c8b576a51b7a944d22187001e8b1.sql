-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "facility_type",
    "category",
    "no_of_units"
FROM "sg-data-d-2657c8b576a51b7a944d22187001e8b1"
