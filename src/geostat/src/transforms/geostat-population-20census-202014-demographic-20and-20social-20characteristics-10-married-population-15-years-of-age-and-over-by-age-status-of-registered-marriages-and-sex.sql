-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "status_of_registred_marriages",
    "urban_rural",
    "age",
    "value"
FROM "geostat-population-20census-202014-demographic-20and-20social-20characteristics-10-married-population-15-years-of-age-and-over-by-age-status-of-registered-marriages-and-sex"
