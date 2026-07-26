-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acres",
    "areatype",
    "borough",
    "cemsdistrict",
    "cemsid",
    "cemsparent",
    "communityboard",
    "councildistrict",
    "gispropnum",
    "_name" AS name,
    "omppropid",
    "parkdistrict",
    "precinct",
    "propertyname",
    "subpropertyname",
    "_system" AS system,
    "zipcode",
    "multipolygon"
FROM "nyc-open-data-c5vm-g2dk"
