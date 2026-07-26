-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "districtcode",
    "objectid",
    "shape_area",
    "shape_length",
    "multipolygon"
FROM "nyc-open-data-i6mn-amj2"
