-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "motor_vehicle_cars",
    CAST("year" AS BIGINT) AS year,
    "fuel_types",
    "value"
FROM "geostat-environment-20statistics-environmental-20indicators-13-h-3"
