-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid",
    "elevation",
    "model",
    "notes",
    "created_user",
    "created_date",
    "last_edited_user",
    "last_edited_date",
    "shape__area" AS shape_area,
    "shape__length" AS shape_length,
    "base_bbl",
    "unit_lot",
    "unit_bbl",
    "unit_designation",
    "bin",
    "condo_key",
    "floor_text",
    "floor_num",
    "room_height",
    "room_desc",
    "base_height",
    "top_height"
FROM "nyc-open-data-b5bf-t8kd"
