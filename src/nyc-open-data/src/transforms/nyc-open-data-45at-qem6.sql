-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid",
    "model",
    "elevation",
    "notes",
    "created_user",
    "created_date",
    "last_edited_user",
    "last_edited_date",
    "shape__area" AS shape_area,
    "shape__length" AS shape_length,
    "parent_boro",
    "parent_block",
    "parent_lot",
    "parent_bbl",
    "air_lot_number",
    "air_lot_bbl"
FROM "nyc-open-data-45at-qem6"
