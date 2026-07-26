-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_zone" AS zone,
    "zonename",
    "borocode",
    "objectid",
    "shape_area",
    "shape_length",
    "multipolygon"
FROM "nyc-open-data-ak2e-nbe8"
