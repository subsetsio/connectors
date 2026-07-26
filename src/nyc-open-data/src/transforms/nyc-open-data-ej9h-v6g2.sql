-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hectare",
    "shift",
    "date",
    "anonymized_sighter",
    "sighter_observed_weather_data",
    "litter",
    "litter_notes",
    "other_animal_sightings",
    "hectare_conditions",
    "hectare_conditions_notes",
    "number_of_sighters",
    "number_of_squirrels",
    "total_time_of_sighting"
FROM "nyc-open-data-ej9h-v6g2"
