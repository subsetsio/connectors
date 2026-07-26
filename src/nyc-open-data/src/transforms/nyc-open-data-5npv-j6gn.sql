-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "communityboard",
    "councildistrict",
    "dispenserunitlocation",
    "gispropnum",
    "installationdate",
    "_location" AS location,
    "manufacturer",
    "mountingsurface",
    "objectid",
    "omppropid",
    "parkdistrict",
    "precinct",
    "propertyname",
    "restockedby",
    "subpropertyname",
    "zipcode",
    "point"
FROM "nyc-open-data-5npv-j6gn"
