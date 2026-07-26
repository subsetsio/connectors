-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "gispropnum",
    "objectid",
    "department",
    "parentid",
    "communityb",
    "councildis",
    "precinct",
    "zipcode",
    "borough",
    "_name" AS name,
    "wf_type",
    "featuresta"
FROM "nyc-open-data-8kvz-b7tv"
