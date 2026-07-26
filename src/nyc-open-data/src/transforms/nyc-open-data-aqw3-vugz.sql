-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "join_count",
    "target_fid",
    "id",
    "fld_zone",
    "static_bfe",
    "abfe_0_2pc",
    "shape_leng",
    "shape_area",
    "gridcode",
    "orig_fid"
FROM "nyc-open-data-aqw3-vugz"
