-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "_name" AS name,
    "borough",
    "link",
    "x_coordinate",
    "y_coordinate"
FROM "nyc-open-data-pxkn-awzt"
