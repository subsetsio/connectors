-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "parking_location",
    "_type" AS type,
    "borough",
    "install_date",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-hjz2-y62k"
