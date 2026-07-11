-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "motor_vehicle_cars",
    CAST("year" AS BIGINT) AS year,
    "age",
    "value"
FROM "geostat-environment-20statistics-environmental-20indicators-14-h-4"
