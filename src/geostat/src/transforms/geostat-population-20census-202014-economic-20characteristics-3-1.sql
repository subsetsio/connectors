-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "activity_status",
    "urban_rural",
    "educational_attainment",
    "value"
FROM "geostat-population-20census-202014-economic-20characteristics-3-1"
