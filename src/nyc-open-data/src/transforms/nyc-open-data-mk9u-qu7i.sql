-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acres",
    "borough",
    "commissiondate",
    "communityboard",
    "councildistrict",
    "department",
    "description",
    "featurestatus",
    "gispropnum",
    "gsgroup",
    "gstype",
    "_location" AS location,
    "mou",
    "nys_assembly",
    "nys_senate",
    "omppropid",
    "parentid",
    "precinct",
    "sitename",
    "starea",
    "stlength",
    "subcategory",
    "_system" AS system,
    "us_congress",
    "zipcode",
    "multipolygon"
FROM "nyc-open-data-mk9u-qu7i"
