-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "car_park_no",
    "address",
    "x_coord",
    "y_coord",
    "car_park_type",
    "type_of_parking_system",
    "short_term_parking",
    "free_parking",
    "night_parking",
    "car_park_decks",
    "gantry_height",
    "car_park_basement"
FROM "sg-data-d-23f946fa557947f93a8043bbef41dd09"
