-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "park_name",
    "borough",
    "gispropnum",
    "shape_area",
    "shape_len"
FROM "nyc-open-data-at6q-ktig"
