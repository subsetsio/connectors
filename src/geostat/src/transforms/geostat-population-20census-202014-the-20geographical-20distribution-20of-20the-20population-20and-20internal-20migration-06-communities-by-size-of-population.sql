-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "size",
    "communities",
    "regions_municipalites",
    "value"
FROM "geostat-population-20census-202014-the-20geographical-20distribution-20of-20the-20population-20and-20internal-20migration-06-communities-by-size-of-population"
