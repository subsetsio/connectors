-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "amenitytype",
    "borough",
    "communityboard",
    "councildistrict",
    "gispropnum",
    "_hours" AS hours,
    "languagecode",
    "mountingsurface",
    "nametext",
    "omppropid",
    "parkdistrict",
    "precinct",
    "propertylocation",
    "propertyname",
    "secondlanguage",
    "signcode",
    "signcodewithlanguage",
    "signstatus",
    "signtype",
    "subpropertyname",
    "_system" AS system,
    "thirdlanguage",
    "zipcode",
    "point"
FROM "nyc-open-data-hv9n-xgy4"
