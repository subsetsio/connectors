-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_speed_camera",
    "location",
    "location_latitude",
    "location_longitude"
FROM "sg-data-d-983804de2bc016f53e44031d85d1ec8a"
