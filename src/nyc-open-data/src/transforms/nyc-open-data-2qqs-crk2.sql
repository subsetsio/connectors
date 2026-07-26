-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "county_fip",
    "shape_area",
    "shape_leng",
    "boro_name",
    "boro_code",
    "target_id"
FROM "nyc-open-data-2qqs-crk2"
