-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_system" AS system,
    "borough",
    "gispropnum",
    "propname",
    "omppropid",
    "sitename",
    "district",
    "councildistrict",
    "point"
FROM "nyc-open-data-ckaz-6gaa"
