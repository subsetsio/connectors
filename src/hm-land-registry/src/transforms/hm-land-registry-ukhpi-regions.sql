-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region_slug",
    "region_uri",
    "region_name",
    "region_type"
FROM "hm-land-registry-ukhpi-regions"
