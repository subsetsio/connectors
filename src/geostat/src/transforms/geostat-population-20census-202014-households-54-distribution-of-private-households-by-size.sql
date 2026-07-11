-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "households_by_size",
    "urban_rural",
    "regions",
    "value"
FROM "geostat-population-20census-202014-households-54-distribution-of-private-households-by-size"
