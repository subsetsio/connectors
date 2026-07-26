-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "zip_code",
    "land_area",
    "water_area",
    "center_latitude",
    "center_longitude",
    "internal_latitude",
    "internal_longitude",
    "geometry"
FROM "nyc-open-data-35j5-n34v"
