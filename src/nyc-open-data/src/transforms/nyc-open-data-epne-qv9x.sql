-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hurricane_evacuation_zone",
    "shape_length",
    "shape_area",
    "the_geom"
FROM "nyc-open-data-epne-qv9x"
