-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "block_id",
    "block_stat",
    "trees",
    "surv_date",
    "group_name",
    "cb_num",
    "borocode",
    "boroname",
    "cncldist",
    "st_assem",
    "st_senate",
    "nta",
    "nta_name",
    "boro_ct",
    "zipcode",
    "zip_city",
    "state",
    "start_x_sp",
    "start_y_sp",
    "mid_x_sp",
    "mid_y_sp",
    "end_x_sp",
    "end_y_sp",
    "start_lat",
    "start_long",
    "mid_lat",
    "mid_long",
    "end_lat",
    "end_long",
    "shape_leng"
FROM "nyc-open-data-ju3b-rwpy"
