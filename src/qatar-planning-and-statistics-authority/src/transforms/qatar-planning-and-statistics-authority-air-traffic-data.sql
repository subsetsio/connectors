-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "aircraft_movement",
    "number_of_passengers",
    "air_cargo_mail"
FROM "qatar-planning-and-statistics-authority-air-traffic-data"
