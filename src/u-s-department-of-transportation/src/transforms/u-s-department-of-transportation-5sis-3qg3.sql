-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("vmt" AS BIGINT) AS vmt,
    CAST("motor_fuel_consumption" AS BIGINT) AS motor_fuel_consumption,
    CAST("miles_per_gallon" AS DOUBLE) AS miles_per_gallon,
    CAST("vehicle_registrations" AS BIGINT) AS vehicle_registrations,
    CAST("gallons_per_vehicle" AS DOUBLE) AS gallons_per_vehicle,
    CAST("vmt_index" AS DOUBLE) AS vmt_index,
    CAST("fuel_index" AS DOUBLE) AS fuel_index,
    CAST("vmt_per_fuel_index" AS DOUBLE) AS vmt_per_fuel_index,
    CAST("vehicles_index" AS DOUBLE) AS vehicles_index,
    CAST("fuel_per_vehicle_index" AS DOUBLE) AS fuel_per_vehicle_index
FROM "u-s-department-of-transportation-5sis-3qg3"
