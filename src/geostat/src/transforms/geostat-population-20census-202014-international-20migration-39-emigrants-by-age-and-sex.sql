-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "urban_rural",
    "age",
    "value"
FROM "geostat-population-20census-202014-international-20migration-39-emigrants-by-age-and-sex"
