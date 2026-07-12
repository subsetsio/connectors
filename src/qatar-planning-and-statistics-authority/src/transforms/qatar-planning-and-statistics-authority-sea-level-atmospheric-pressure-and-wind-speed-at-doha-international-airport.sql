-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("year_month", '%Y-%m')::DATE AS year_month,
    "average_of_minumum_atmospheric_pressure_hetopascal",
    "average_of_maximum_atmospheric_pressure_hetopascal",
    "average_wind_speed_knots",
    "average_of_maximum_wind_speed_knots"
FROM "qatar-planning-and-statistics-authority-sea-level-atmospheric-pressure-and-wind-speed-at-doha-international-airport"
