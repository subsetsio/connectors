-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "urban_rural",
    "country_of_usual_residence",
    "value"
FROM "geostat-population-20census-202014-international-20migration-46-emigrants-by-country-of-current-residence-and-sex"
