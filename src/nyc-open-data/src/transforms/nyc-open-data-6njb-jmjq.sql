-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "gispropnum",
    "omppropid",
    "objectid",
    "department",
    "_location" AS location,
    "communityb",
    "councildis",
    "precinct",
    "zipcode",
    "borough",
    "shape_star",
    "shape_stle"
FROM "nyc-open-data-6njb-jmjq"
