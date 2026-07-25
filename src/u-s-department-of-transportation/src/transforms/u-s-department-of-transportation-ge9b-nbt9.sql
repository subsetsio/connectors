-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "beginning_cross_street",
    "core_details",
    CAST("end_date" AS TIMESTAMP) AS end_date,
    "ending_cross_street",
    CAST("is_end_date_verified" AS BOOLEAN) AS is_end_date_verified,
    CAST("is_end_position_verified" AS BOOLEAN) AS is_end_position_verified,
    CAST("is_start_date_verified" AS BOOLEAN) AS is_start_date_verified,
    CAST("is_start_position_verified" AS BOOLEAN) AS is_start_position_verified,
    "line",
    "location_method",
    CAST("start_date" AS TIMESTAMP) AS start_date,
    "vehicle_impact"
FROM "u-s-department-of-transportation-ge9b-nbt9"
