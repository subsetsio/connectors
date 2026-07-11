-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age",
    "sex",
    "citizenship",
    "value"
FROM "geostat-population-20census-202014-international-20migration-26-population-by-citizenship-country-and-age"
