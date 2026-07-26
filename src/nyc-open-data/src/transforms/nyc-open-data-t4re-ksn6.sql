-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "communityboard",
    "councildistrict",
    "objectid",
    "parkdistricts",
    "sector",
    "multipolygon"
FROM "nyc-open-data-t4re-ksn6"
