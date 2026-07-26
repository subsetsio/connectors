-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "ntaname",
    "sitename",
    "siteaddress",
    "categoriesaccepted",
    "categoriesavailable",
    "moreinfo",
    "pickupstatus",
    "_hours" AS hours,
    "website",
    "phonenumber",
    "email",
    "partner",
    "dsny_zone",
    "dsny_district",
    "dsny_section",
    "borocd",
    "community_district",
    "councildistrict",
    "senate_district",
    "congressional_district",
    "assembly_district",
    "policeprecinct",
    "bbl",
    "bin",
    "census_tract",
    "latitude",
    "longitude",
    "objectid",
    "point"
FROM "nyc-open-data-gkgs-za6m"
