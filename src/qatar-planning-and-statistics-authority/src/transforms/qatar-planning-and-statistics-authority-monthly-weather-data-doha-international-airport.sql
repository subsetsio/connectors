-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("month", '%Y-%m')::DATE AS month,
    "average_of_maximum_temperature_oc",
    "average_of_minimum_temperature_oc",
    "mean_wind_speed_knots",
    "average_relative_humidity",
    "msl_pressure_hpa"
FROM "qatar-planning-and-statistics-authority-monthly-weather-data-doha-international-airport"
