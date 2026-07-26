-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid",
    "borough",
    "school_nam",
    "on_street",
    "from_stree",
    "to_street",
    "open_date",
    "nhoodname",
    "segmentid",
    "shape_leng",
    "shape_stle"
FROM "nyc-open-data-vtjm-ngnu"
