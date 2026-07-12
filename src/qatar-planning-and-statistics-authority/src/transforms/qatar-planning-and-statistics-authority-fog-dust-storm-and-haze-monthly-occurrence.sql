-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lshhr",
    "month",
    "lzhr_ljwy",
    "weather_phenomenon",
    "value"
FROM "qatar-planning-and-statistics-authority-fog-dust-storm-and-haze-monthly-occurrence"
