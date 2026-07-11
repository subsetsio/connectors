-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "urban_rural",
    "disability_status",
    "regions",
    "value"
FROM "geostat-population-20census-202014-disability-51-distribution-of-population-by-regions-urban-rural-settlements-and-disability-status"
