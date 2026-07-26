-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_zone" AS zone,
    "zone_name",
    "cd",
    "objectid",
    "shape_area",
    "shape_length",
    "multipolygon"
FROM "nyc-open-data-8ev8-jjxq"
