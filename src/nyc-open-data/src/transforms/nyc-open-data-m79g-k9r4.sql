-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geometry",
    "boro",
    "status",
    "projectnam",
    "dateadopte",
    "zr_ulurpno",
    "zr_map",
    "cd",
    "mih_option",
    "zoning_map",
    "project_id",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-m79g-k9r4"
