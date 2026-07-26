-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "objectid",
    "_system" AS system,
    "the_geom",
    "gispropnum",
    "department",
    "parentid",
    "communityboard",
    "councildistrict",
    "precinct",
    "zipcode",
    "borough",
    "dog_area_type",
    "_name" AS name,
    "seating",
    "surface",
    "featurestatus"
FROM "nyc-open-data-hxx3-bwgv"
