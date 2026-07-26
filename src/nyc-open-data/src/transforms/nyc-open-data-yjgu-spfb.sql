-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_" AS number,
    "image",
    "objectid",
    "the_geom",
    "curr_round",
    "curr_user",
    "curr_stat",
    "curr_err",
    "borough",
    "shape_area",
    "shape_len",
    "boro"
FROM "nyc-open-data-yjgu-spfb"
