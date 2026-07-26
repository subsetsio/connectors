-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gispropnum",
    "_system" AS system,
    "the_geom",
    "objectid",
    "_name" AS name,
    "_comments" AS comments,
    "_location" AS location,
    "featuresta",
    "department",
    "communityb",
    "councildis",
    "precinct",
    "zipcode",
    "borough",
    "acres",
    "gisobjid",
    "expr1"
FROM "nyc-open-data-xvww-awjk"
