-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "flat_type",
    "type_of_family_nucleus",
    "percentage"
FROM "sg-data-d-e31c9070e0b1363584683b81d984bfa7"
