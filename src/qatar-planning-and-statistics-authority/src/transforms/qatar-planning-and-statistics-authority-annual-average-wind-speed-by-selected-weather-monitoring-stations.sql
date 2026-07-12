-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mesaieed",
    "ruwais",
    "dukhan",
    "doha_intl_airport",
    "karaana"
FROM "qatar-planning-and-statistics-authority-annual-average-wind-speed-by-selected-weather-monitoring-stations"
