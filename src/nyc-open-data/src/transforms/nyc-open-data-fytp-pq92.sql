-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "physicalid",
    "l_low_hn",
    "l_high_hn",
    "r_low_hn",
    "r_high_hn",
    "l_zip",
    "r_zip",
    "l_blkfc_id",
    "r_blkfc_id",
    "st_label",
    "status",
    "bike_lane",
    "borocode",
    "st_width",
    "created",
    "modified",
    "trafdir",
    "rw_type",
    "frm_lvl_co",
    "to_lvl_co",
    "snow_pri",
    "pre_modifi",
    "pre_direct",
    "pre_type",
    "post_type",
    "post_direc",
    "post_modif",
    "full_stree",
    "st_name",
    "bike_trafd",
    "shape_leng"
FROM "nyc-open-data-fytp-pq92"
