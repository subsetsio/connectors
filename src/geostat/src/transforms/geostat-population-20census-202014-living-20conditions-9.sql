-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_room",
    "size_of_private_households",
    "urban_rural",
    "region",
    "value"
FROM "geostat-population-20census-202014-living-20conditions-9"
