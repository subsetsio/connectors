-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "boro",
    "status",
    "projectnam",
    "dateadopte",
    "zr_map",
    "leadaction",
    "cd",
    "shape_star",
    "shape_stle",
    "shape_leng",
    "shape_area"
FROM "nyc-open-data-e9rz-c67w"
