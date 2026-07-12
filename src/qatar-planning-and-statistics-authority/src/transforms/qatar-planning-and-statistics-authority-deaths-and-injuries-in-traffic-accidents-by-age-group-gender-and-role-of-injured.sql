-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_groups",
    "age_groups_ar",
    "death_driver_males",
    "death_driver_females",
    "death_passenger_males",
    "death_passenger_females",
    "death_pedestrians_males",
    "death_pedestrians_females",
    "severe_injury_driver_males",
    "severe_injury_driver_females",
    "severe_injury_passenger_males",
    "severe_injury_passenger_females",
    "severe_injury_pedestrians_males",
    "severe_injury_pedestrians_females",
    "slight_injury_driver_males",
    "slight_injury_driver_females",
    "slight_injury_passenger_males",
    "slight_injury_pedestrians_males",
    "slight_injury_passenger_females",
    "slight_injury_pedestrians_females"
FROM "qatar-planning-and-statistics-authority-deaths-and-injuries-in-traffic-accidents-by-age-group-gender-and-role-of-injured"
