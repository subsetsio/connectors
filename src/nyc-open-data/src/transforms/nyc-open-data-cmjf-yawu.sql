-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "schooldist",
    "boro",
    "initials",
    "creat_date",
    "edit_date",
    "boro_num",
    "shape_leng",
    "shape_area",
    "remarks",
    "dbn",
    "esid_no",
    "_label" AS label,
    "zoned_dist",
    "x_centroid",
    "y_centroid"
FROM "nyc-open-data-cmjf-yawu"
