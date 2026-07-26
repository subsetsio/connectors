-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "objectid",
    "bbl",
    "shape_area",
    "shape_length",
    "address",
    "material",
    "record_type",
    "city_owned"
FROM "nyc-open-data-jqfp-uff7"
