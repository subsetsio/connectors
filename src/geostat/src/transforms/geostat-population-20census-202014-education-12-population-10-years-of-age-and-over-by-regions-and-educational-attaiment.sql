-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "educational_attaiment",
    "urban_rural",
    "regions",
    "value"
FROM "geostat-population-20census-202014-education-12-population-10-years-of-age-and-over-by-regions-and-educational-attaiment"
