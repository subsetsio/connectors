-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hour_beginning",
    "_location" AS location,
    "pedestrians",
    "towards_manhattan",
    "towards_brooklyn",
    "weather_summary",
    "temperature",
    "precipitation",
    "lat",
    "long",
    "events",
    "location1"
FROM "nyc-open-data-6fi9-q3ta"
