-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "month_ar",
    "2020_relative_humidity_min",
    "2020_relative_humidity_max",
    "2020_average_temperature_degc_min",
    "2020_average_temperature_degc_max",
    "2021_relative_humidity_min",
    "2021_relative_humidity_max",
    "2021_average_temperature_degc_min",
    "2021_average_temperature_degc_max",
    "2022_relative_humidity_min",
    "2022_relative_humidity_max",
    "2022_average_temperature_degc_min",
    "2022_average_temperature_degc_max",
    "2023_relative_humidity_min",
    "2023_relative_humidity_max",
    "2023_average_temperature_degc_min",
    "2023_average_temperature_degc_max",
    "2024_relative_humidity_min",
    "2024_relative_humidity_max",
    "2024_average_temperature_degc_min",
    "2024_average_temperature_degc_max"
FROM "qatar-planning-and-statistics-authority-maximum-minimum-temperature-and-monthly-relative-humidity-doha-international-airport"
