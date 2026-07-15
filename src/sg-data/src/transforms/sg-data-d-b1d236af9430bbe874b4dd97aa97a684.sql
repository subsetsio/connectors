-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "company_name",
    "licensee_name",
    "license_effective_date",
    "license_expiry_date",
    "license_type",
    "category_of_poisons",
    "specific_details"
FROM "sg-data-d-b1d236af9430bbe874b4dd97aa97a684"
