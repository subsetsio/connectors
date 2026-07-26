-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid",
    "boro",
    "block",
    "lot",
    "bbl",
    "condo_flag",
    "reuc_flag",
    "air_lot_flag",
    "sub_lot_flag",
    "easement_flag",
    "lot_note",
    "effective_tax_year",
    "bill_bbl_flag",
    "nycmap_bldg_flag",
    "conversion_exception_flag",
    "value_reflected_out_flag",
    "created_user",
    "created_date",
    "last_edited_user",
    "last_edited_date",
    "shape__area" AS shape_area,
    "shape__length" AS shape_length
FROM "nyc-open-data-nst5-iqiu"
