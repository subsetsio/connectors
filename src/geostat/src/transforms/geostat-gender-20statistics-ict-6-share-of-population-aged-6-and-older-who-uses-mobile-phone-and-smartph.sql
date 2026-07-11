-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "usage",
    "year",
    "age",
    "value"
FROM "geostat-gender-20statistics-ict-6-share-of-population-aged-6-and-older-who-uses-mobile-phone-and-smartph"
