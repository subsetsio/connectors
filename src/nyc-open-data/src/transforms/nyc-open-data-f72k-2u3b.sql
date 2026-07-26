-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "shape_leng",
    "boro_code",
    "boro_name",
    "_zone" AS zone,
    "zone_name",
    "rate_zone",
    "shape_le_1",
    "shape_area"
FROM "nyc-open-data-f72k-2u3b"
