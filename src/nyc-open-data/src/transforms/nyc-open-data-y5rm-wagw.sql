-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "communityboard",
    "councildistrict",
    "parkdistrict",
    "gispropnum",
    "_location" AS location,
    "_name" AS name,
    "omppropid",
    "_system" AS system,
    "polygon",
    "pooltype"
FROM "nyc-open-data-y5rm-wagw"
