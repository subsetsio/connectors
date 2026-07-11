-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "previous_country_of_residence",
    "urban_rural",
    "usual_place_of_residence",
    "value"
FROM "geostat-population-20census-202014-international-20migration-29-2-immigrants-by-previous-country-of-residence-and-usual-place-of-residence"
