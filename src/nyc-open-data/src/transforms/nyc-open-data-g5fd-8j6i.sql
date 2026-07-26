-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "gispropnum",
    "communityb",
    "councildis",
    "precinct",
    "zipcode",
    "borough",
    "signname",
    "shape_star",
    "shape_stle"
FROM "nyc-open-data-g5fd-8j6i"
