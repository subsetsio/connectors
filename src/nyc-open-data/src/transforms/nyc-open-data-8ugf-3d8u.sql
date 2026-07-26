-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_district",
    "shape_length",
    "shape_area",
    "the_geom"
FROM "nyc-open-data-8ugf-3d8u"
