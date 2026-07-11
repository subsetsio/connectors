-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ethnicity",
    "urban_rural",
    "regions",
    "value"
FROM "geostat-population-20census-202014-demographic-20and-20social-20characteristics-17-total-population-by-regions-and-ethnicity"
