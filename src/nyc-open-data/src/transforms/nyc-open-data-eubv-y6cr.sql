-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gispropnum",
    "_system" AS system,
    "the_geom",
    "objectid",
    "department",
    "parentid",
    "communityb",
    "councildis",
    "precinct",
    "zipcode",
    "borough",
    "ladder_id",
    "ladder_cou",
    "featuresta"
FROM "nyc-open-data-eubv-y6cr"
