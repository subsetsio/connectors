-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid",
    "boro",
    "block",
    "section_number",
    "volume_number",
    "eop_overlap_flag",
    "jagged_st_flag",
    "created_user",
    "created_date",
    "last_edited_user",
    "last_edited_date",
    "shape__area" AS shape_area,
    "shape__length" AS shape_length
FROM "nyc-open-data-ku5s-ingk"
