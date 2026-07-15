-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rent_approval_date",
    "town",
    "block",
    "street_name",
    "flat_type",
    "monthly_rent"
FROM "sg-data-d-c9f57187485a850908655db0e8cfe651"
