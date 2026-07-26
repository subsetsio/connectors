-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shape_geometry",
    "shape_length",
    "shape_area",
    "_zone" AS zone,
    "location_id",
    "borough"
FROM "nyc-open-data-8meu-9t5y"
