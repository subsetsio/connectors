-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "gridcode",
    "join_count",
    "fld_zone",
    "static_bfe",
    "abfe_0_2pc",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-27ya-gqtm"
