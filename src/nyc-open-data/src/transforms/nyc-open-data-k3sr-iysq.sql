-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_system" AS system,
    "objectid",
    "the_geom",
    "gispropnum",
    "department",
    "parentid",
    "_location" AS location,
    "communityb",
    "councildis",
    "precinct",
    "zipcode",
    "borough",
    "avlparking",
    "launchland",
    "_name" AS name,
    "parks",
    "_storage" AS storage,
    "featuresta"
FROM "nyc-open-data-k3sr-iysq"
