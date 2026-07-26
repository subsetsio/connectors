-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acres",
    "borough",
    "communityboard",
    "councildistrict",
    "department",
    "description",
    "gispropnum",
    "_location" AS location,
    "nys_assembly",
    "nys_senate",
    "omppropid",
    "precinct",
    "propname",
    "retired",
    "retireddate",
    "sitename",
    "subcategory",
    "us_congress",
    "zipcode",
    "multipolygon"
FROM "nyc-open-data-4j29-i5ry"
