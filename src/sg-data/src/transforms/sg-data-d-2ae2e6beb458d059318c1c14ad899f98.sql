-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "brand_name",
    "product_name",
    "dosage_form",
    "company_name",
    "manufacturer",
    "country_of_manufacturer"
FROM "sg-data-d-2ae2e6beb458d059318c1c14ad899f98"
