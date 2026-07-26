-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "ntaname",
    "sitename",
    "siteaddress",
    "zipcode",
    "dsnyzone",
    "dsnydistrict",
    "dsnysection",
    "communitydistrict",
    "boroct2020",
    "councildistrict",
    "senatedistrict",
    "congressionaldistrict",
    "assemblydistrict",
    "policeprecinct",
    "bbl",
    "bin",
    "latitude",
    "longitude",
    "objectid",
    "point"
FROM "nyc-open-data-wshr-5vic"
