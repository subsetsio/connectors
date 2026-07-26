-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "schooldist",
    "initials",
    "creat_date",
    "edit_date",
    "boro",
    "shape_leng",
    "shape_area",
    "boro_text",
    "dbn",
    "remarks",
    "msid_no",
    "_label" AS label,
    "zoned_dist"
FROM "nyc-open-data-t26j-jbq7"
