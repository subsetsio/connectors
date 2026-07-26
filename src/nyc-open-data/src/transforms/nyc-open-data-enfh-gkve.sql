-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acquisitiondate",
    "acres",
    "address",
    "borough",
    "_class" AS class,
    "communityboard",
    "councildistrict",
    "department",
    "gisobjid",
    "gispropnum",
    "globalid",
    "jurisdiction",
    "_location" AS location,
    "mapped",
    "name311",
    "nys_assembly",
    "nys_senate",
    "objectid",
    "omppropid",
    "parentid",
    "permit",
    "permitdistrict",
    "permitparent",
    "pip_ratable",
    "precinct",
    "retired",
    "signname",
    "subcategory",
    "typecategory",
    "us_congress",
    "waterfront",
    "zipcode",
    "multipolygon"
FROM "nyc-open-data-enfh-gkve"
