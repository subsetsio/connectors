-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_ownership",
    "individual_houses_separate_apartments",
    "urban_rural",
    "region",
    "value"
FROM "geostat-population-20census-202014-living-20conditions-6-2"
